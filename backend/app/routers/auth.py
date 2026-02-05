from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from datetime import timedelta, datetime
import secrets
import random
from ..mongo import get_mongo_db, get_next_sequence
from ..models import UserRole
from ..schemas import UserCreate, UserResponse, LoginRequest, Token
from ..auth import (
    authenticate_user, 
    create_access_token, 
    create_refresh_token,
    get_password_hash,
    get_current_active_user,
    verify_password,
)
from ..config import settings
from ..logger import green_logger
from ..email_service import email_service
from ..security import (
    sanitize_string, validate_email, validate_username,
    sanitize_code_content
)

router = APIRouter()

# Import shared rate limiter
from ..rate_limiter import limiter


def _generate_otp(length: int = 6) -> str:
    """Generate a numeric OTP of given length."""
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


@router.post("/signup", response_model=UserResponse)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def signup(request: Request, user_data: UserCreate, db=Depends(get_mongo_db)):
    """Register a new user"""
    # Validate and sanitize input
    if not validate_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    if not validate_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be 3-30 characters and contain only letters, numbers, underscores, or hyphens"
        )
    
    # Sanitize inputs
    user_data.email = sanitize_string(user_data.email.lower().strip())
    user_data.username = sanitize_string(user_data.username.strip())
    
    # Validate password strength
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    # Check if user already exists
    existing_user = await db["users"].find_one(
        {"$or": [{"email": user_data.email}, {"username": user_data.username}]}
    )
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    # Generate verification OTP (6 digits) valid for 10 minutes
    otp_code = _generate_otp(6)
    otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user_id = await get_next_sequence(db, "users")
    db_user = {
        "id": user_id,
        "email": user_data.email,
        "username": user_data.username,
        "hashed_password": hashed_password,
        "role": (user_data.role or UserRole.DEVELOPER).value,
        "is_active": True,
        "is_verified": False,
        "otp": otp_code,
        "otp_expiry": otp_expiry,
        "email_verification_token": None,
        "password_reset_token": None,
        "password_reset_expires": None,
        "current_streak": 0,
        "longest_streak": 0,
        "last_submission_date": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    try:
        await db["users"].insert_one(db_user)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create user account. Email or username may already exist.",
        )
    
    # Send OTP email
    try:
        email_service.send_signup_otp_email(
            to_email=user_data.email,
            otp=otp_code,
            username=user_data.username,
            expiry_minutes=10
        )
    except Exception as e:
        green_logger.logger.warning(f"Failed to send signup OTP email: {e}")
    
    # Log user registration
    green_logger.log_user_action(
        user_id=db_user["id"],
        action="user_registered",
        details={"email": user_data.email, "role": db_user["role"]},
    )
    
    return UserResponse.model_validate(db_user)


@router.post("/login", response_model=Token)
# Use a relaxed limit outside production to keep automated tests stable
@limiter.limit("1000/minute" if settings.environment.lower() != "production" else "10/minute")
async def login(request: Request, login_data: LoginRequest, db=Depends(get_mongo_db)):
    """Authenticate user and return tokens"""
    try:
        # Sanitize email input
        login_data.email = sanitize_string(login_data.email.lower().strip())
        
        if not validate_email(login_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )

        # Find user first to differentiate errors
        user = await db["users"].find_one({"email": login_data.email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check password explicitly for better messaging
        if not verify_password(login_data.password, user.get("hashed_password", "")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )

        if not user.get("is_verified", False):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account not verified. Please verify the OTP sent to your email."
            )
        
        # Create tokens
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user["username"]}, expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(data={"sub": user["username"]})
        
        # Log successful login
        green_logger.log_user_action(
            user_id=user["id"],
            action="user_login",
            details={"email": user["email"]},
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the actual error for debugging
        green_logger.log_error(e, {
            "path": str(request.url.path),
            "method": request.method,
            "email": login_data.email if hasattr(login_data, 'email') else None
        })
        # Return a more helpful error message in development
        error_detail = str(e) if settings.debug else "Database connection error. Please check your MongoDB configuration."
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user=Depends(get_current_active_user)):
    """Get current user information"""
    return UserResponse.model_validate(current_user)


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db=Depends(get_mongo_db)):
    """Refresh access token using refresh token"""
    # This would need proper refresh token validation
    # For now, return a placeholder
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Refresh token functionality not yet implemented"
    )


@router.post("/logout")
async def logout(current_user=Depends(get_current_active_user)):
    """Logout user (client should discard tokens)"""
    green_logger.log_user_action(
        user_id=current_user.id,
        action="user_logout",
        details={"email": current_user.email},
    )
    
    return {"message": "Successfully logged out"}


@router.post("/verify-email")
async def verify_email(token: str = Form(...), db=Depends(get_mongo_db)):
    """Verify user email with token"""
    user = await db["users"].find_one({"email_verification_token": token})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    if user.get("is_verified"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )
    
    # Verify user
    await db["users"].update_one(
        {"id": user["id"]},
        {
            "$set": {
                "is_verified": True,
                "email_verification_token": None,
                "updated_at": datetime.utcnow(),
            }
        },
    )
    
    green_logger.log_user_action(
        user_id=user["id"],
        action="email_verified",
        details={"email": user["email"]},
    )
    
    return {"message": "Email verified successfully"}


@router.post("/verify-otp")
async def verify_otp(email: str = Form(...), otp: str = Form(...), db=Depends(get_mongo_db)):
    """Verify email using OTP code"""
    user = await db["users"].find_one({"email": email})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or OTP"
        )
    
    if user.get("is_verified"):
        return {"message": "Account already verified"}
    
    stored_otp = user.get("otp")
    otp_expiry = user.get("otp_expiry")
    
    if not stored_otp or not otp_expiry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No OTP found. Please request a new one."
        )
    
    if otp != stored_otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )
    
    if otp_expiry < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired"
        )
    
    # Mark verified and clear OTP
    await db["users"].update_one(
        {"id": user["id"]},
        {
            "$set": {
                "is_verified": True,
                "otp": None,
                "otp_expiry": None,
                "updated_at": datetime.utcnow(),
            }
        },
    )
    
    green_logger.log_user_action(
        user_id=user["id"],
        action="otp_verified",
        details={"email": user["email"]},
    )
    
    return {"message": "OTP verified successfully"}


@router.post("/forgot-password")
async def forgot_password(email: str = Form(...), db=Depends(get_mongo_db)):
    """Send password reset email"""
    user = await db["users"].find_one({"email": email})
    if not user:
        # Don't reveal if email exists or not
        return {"message": "If the email exists, a reset link has been sent"}
    
    # Generate reset token
    reset_token = secrets.token_urlsafe(32)
    reset_expires = datetime.utcnow() + timedelta(minutes=15)
    
    # Save reset token
    await db["users"].update_one(
        {"id": user["id"]},
        {
            "$set": {
                "password_reset_token": reset_token,
                "password_reset_expires": reset_expires,
                "reset_token": reset_token,
                "reset_token_expiry": reset_expires,
                "updated_at": datetime.utcnow(),
            }
        },
    )
    
    # Send reset email
    try:
        email_service.send_password_reset_email(
            to_email=user["email"],
            reset_token=reset_token,
            username=user["username"],
        )
    except Exception as e:
        green_logger.logger.warning(f"Failed to send password reset email: {e}")
    
    # Log password reset request
    green_logger.log_user_action(
        user_id=user["id"],
        action="password_reset_requested",
        details={"email": email}
    )
    
    return {"message": "If the email exists, a reset link has been sent"}


@router.post("/reset-password")
async def reset_password(
    token: str = Form(...), new_password: str = Form(...), db=Depends(get_mongo_db)
):
    """Reset password with token"""
    user = await db["users"].find_one({"$or": [{"password_reset_token": token}, {"reset_token": token}]})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Check if token expired
    expiry = user.get("password_reset_expires") or user.get("reset_token_expiry")
    if expiry and expiry < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )
    
    # Validate new password
    try:
        # Validate password strength
        import re
        pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'
        if not re.match(pattern, new_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters, include 1 uppercase, 1 digit, and 1 special character"
            )
    except HTTPException:
        raise
    except Exception:
        pass
    
    # Update password
    hashed = get_password_hash(new_password)
    await db["users"].update_one(
        {"id": user["id"]},
        {
            "$set": {
                "hashed_password": hashed,
                "password_reset_token": None,
                "password_reset_expires": None,
                "reset_token": None,
                "reset_token_expiry": None,
                "updated_at": datetime.utcnow(),
            }
        },
    )
    
    # Log password reset
    green_logger.log_user_action(
        user_id=user["id"],
        action="password_reset",
        details={"email": user["email"]},
    )
    
    return {"message": "Password reset successfully"}


