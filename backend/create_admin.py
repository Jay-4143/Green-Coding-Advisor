"""
Script to create an admin account in the Green Coding Advisor system.
Usage: python create_admin.py
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from app.mongo import get_mongo_client, get_next_sequence
from app.auth import get_password_hash
from app.models import UserRole
from app.config import settings
from datetime import datetime


async def create_admin():
    """Create an admin user account"""
    print("=" * 50)
    print("Create Admin Account")
    print("=" * 50)
    print()
    
    # Get user input
    email = input("Enter admin email: ").strip()
    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()
    
    if not email or not username or not password:
        print("❌ Error: All fields are required!")
        return False
    
    # Validate password strength
    if len(password) < 8:
        print("❌ Error: Password must be at least 8 characters long!")
        return False
    
    # Get database connection
    client = get_mongo_client()
    db = client[settings.mongodb_db]
    
    # Check if user already exists
    existing_user = await db["users"].find_one(
        {"$or": [{"email": email.lower()}, {"username": username}]}
    )
    
    if existing_user:
        print(f"❌ Error: User with email '{email}' or username '{username}' already exists!")
        print("Would you like to update this user to admin? (y/n): ", end="")
        choice = input().strip().lower()
        
        if choice == 'y':
            # Update existing user to admin
            await db["users"].update_one(
                {"$or": [{"email": email.lower()}, {"username": username}]},
                {"$set": {
                    "role": UserRole.ADMIN.value,
                    "is_active": True,
                    "is_verified": True,
                    "updated_at": datetime.utcnow()
                }}
            )
            print(f"✅ User '{username}' has been updated to admin role!")
            return True
        else:
            print("Operation cancelled.")
            return False
    
    # Create new admin user
    try:
        hashed_password = get_password_hash(password)
        user_id = await get_next_sequence(db, "users")
        
        admin_user = {
            "id": user_id,
            "email": email.lower(),
            "username": username,
            "hashed_password": hashed_password,
            "role": UserRole.ADMIN.value,
            "is_active": True,
            "is_verified": True,  # Auto-verify admin accounts
            "email_verification_token": None,
            "password_reset_token": None,
            "password_reset_expires": None,
            "current_streak": 0,
            "longest_streak": 0,
            "last_submission_date": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        
        await db["users"].insert_one(admin_user)
        
        print()
        print("=" * 50)
        print("✅ Admin account created successfully!")
        print("=" * 50)
        print(f"Email: {email}")
        print(f"Username: {username}")
        print(f"Role: {UserRole.ADMIN.value}")
        print(f"User ID: {user_id}")
        print()
        print("You can now log in with these credentials.")
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin account: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(create_admin())
    sys.exit(0 if success else 1)

