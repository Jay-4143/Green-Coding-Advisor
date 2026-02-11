from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import time
import traceback
from contextlib import asynccontextmanager

from .config import settings
from .logger import green_logger
from .mongo import get_mongo_db
from .routers import auth, submissions, metrics, advisor, chatbot, projects, teams, badges, reports, streaks, admin, contact
from .badge_service import badge_service
from .security import security_middleware


# Initialize MongoDB and default badges
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    green_logger.logger.info("Connecting to MongoDB...")
    
    # Validate production configuration
    if settings.is_production():
        validation_errors = settings.validate_production()
        if validation_errors:
            error_msg = "Production configuration errors detected:\n" + "\n".join(f"  - {err}" for err in validation_errors)
            green_logger.logger.error(error_msg)
            raise RuntimeError(f"Invalid production configuration. {error_msg}")
        green_logger.logger.info("Production configuration validated successfully")
    
    # Initialize default badges and indexes
    try:
        db = await get_mongo_db().__anext__()
        await badge_service.initialize_default_badges(db)
        green_logger.logger.info("Default badges initialized")
        
        # Create MongoDB indexes
        from .mongo_indexes import create_indexes
        indexes = await create_indexes(db)
        green_logger.logger.info(f"MongoDB indexes created: {len(indexes)} indexes")
    except Exception as e:
        green_logger.logger.warning(f"Failed to initialize badges or indexes: {e}")
    
    yield
    # Shutdown
    green_logger.logger.info("Application shutting down")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Green Coding Advisor API",
        description="AI-enhanced web platform for sustainable coding practices",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None
    )

    # Initialize and add rate limiter
    try:
        from .rate_limiter import limiter
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        app.add_middleware(SlowAPIMiddleware)
        green_logger.logger.info("Rate limiter initialized successfully")
    except Exception as e:
        green_logger.logger.warning(f"Rate limiter initialization failed: {e}. Continuing without rate limiting.")

    # Security headers middleware (must be before CORS)
    app.middleware("http")(security_middleware)

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Total-Count", "X-Page", "X-Per-Page"],
    )

    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        
        # Log request
        green_logger.log_api_request(
            method=request.method,
            path=str(request.url.path),
            user_id=getattr(request.state, 'user_id', None)
        )
        
        response = await call_next(request)
        
        # Log response
        process_time = (time.time() - start_time) * 1000
        green_logger.log_performance(
            operation=f"{request.method} {request.url.path}",
            duration_ms=process_time
        )
        
        return response

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        green_logger.log_error(exc, {
            "path": str(request.url.path),
            "method": request.method,
            "traceback": traceback.format_exc()
        })
        
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later.",
                "request_id": getattr(request.state, 'request_id', None)
            }
        )

    # Register error handlers
    from .error_handlers import register_error_handlers
    register_error_handlers(app)

    # Include routers
    app.include_router(auth.router, prefix="/auth", tags=["Authentication"]) 
    app.include_router(submissions.router, prefix="/submissions", tags=["Code Submissions"]) 
    app.include_router(metrics.router, prefix="/metrics", tags=["Metrics & Analytics"]) 
    app.include_router(advisor.router, prefix="/advisor", tags=["AI Advisor"]) 
    app.include_router(chatbot.router, prefix="/chat", tags=["AI Chatbot"]) 
    app.include_router(projects.router, prefix="/projects", tags=["Projects"]) 
    app.include_router(teams.router, prefix="/teams", tags=["Team Collaboration"])
    app.include_router(badges.router, prefix="/badges", tags=["Badges & Achievements"])
    app.include_router(reports.router, prefix="/reports", tags=["Reports"])
    app.include_router(streaks.router, prefix="/streaks", tags=["Streaks"])
    app.include_router(contact.router, prefix="/contact", tags=["Contact"])
    app.include_router(admin.router, prefix="/admin", tags=["Admin"]) 

    @app.get("/health", tags=["Health"])
    async def health():
        return {
            "status": "healthy",
            "version": "1.0.0",
            "environment": settings.environment,
            "timestamp": time.time()
        }

    @app.get("/", tags=["Root"])
    def root():
        return {
            "message": "Welcome to Green Coding Advisor API",
            "version": "1.0.0",
            "docs": "/docs" if settings.debug else "Documentation not available in production",
            "health": "/health"
        }

    return app


app = create_app()
