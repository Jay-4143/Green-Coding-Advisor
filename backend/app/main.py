from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time
import traceback
from contextlib import asynccontextmanager

from .config import settings
from .logger import green_logger
from .database import engine, Base
from .routers import auth, submissions, metrics, advisor, chatbot, projects, teams


# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    green_logger.logger.info("Database tables created successfully")
    yield
    # Shutdown
    green_logger.logger.info("Application shutting down")


# Rate limiter
limiter = Limiter(key_func=get_remote_address)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Green Coding Advisor API",
        description="AI-enhanced web platform for sustainable coding practices",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None
    )

    # Add rate limiter
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
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

    # Validation error handler
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation error",
                "message": "Invalid request data",
                "details": exc.errors()
            }
        )

    # Include routers
    app.include_router(auth.router, prefix="/auth", tags=["Authentication"]) 
    app.include_router(submissions.router, prefix="/submissions", tags=["Code Submissions"]) 
    app.include_router(metrics.router, prefix="/metrics", tags=["Metrics & Analytics"]) 
    app.include_router(advisor.router, prefix="/advisor", tags=["AI Advisor"]) 
    app.include_router(chatbot.router, prefix="/chat", tags=["AI Chatbot"]) 
    app.include_router(projects.router, prefix="/projects", tags=["Projects"]) 
    app.include_router(teams.router, prefix="/teams", tags=["Team Collaboration"]) 

    @app.get("/health", tags=["Health"])
    @limiter.limit("10/minute")
    def health(request: Request):
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


