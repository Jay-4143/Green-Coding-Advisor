from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pymongo.errors import PyMongoError, DuplicateKeyError
from typing import Dict, Any
from .logger import green_logger

def create_error_response(
    status_code: int,
    message: str,
    details: Dict[str, Any] = None,
    error_type: str = None
) -> JSONResponse:
    """Create a standardized error response"""
    error_response = {
        "error": True,
        "message": message,
        "status_code": status_code,
        "error_type": error_type or "application_error"
    }
    
    if details:
        error_response["details"] = details
    
    return JSONResponse(
        status_code=status_code,
        content=error_response
    )


def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    green_logger.log_error(
        exc,
        {
            "path": str(request.url.path),
            "method": request.method,
            "errors": errors
        }
    )
    
    return create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Validation error",
        details={"validation_errors": errors},
        error_type="validation_error"
    )


def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions"""
    green_logger.log_error(
        exc,
        {
            "path": str(request.url.path),
            "method": request.method,
            "status_code": exc.status_code
        }
    )
    
    return create_error_response(
        status_code=exc.status_code,
        message=exc.detail,
        error_type="http_error"
    )


def handle_database_error(request: Request, exc: PyMongoError) -> JSONResponse:
    """Handle MongoDB database errors"""
    from .config import settings
    
    green_logger.log_error(
        exc,
        {
            "path": str(request.url.path),
            "method": request.method,
            "error_type": type(exc).__name__,
            "error_message": str(exc)
        }
    )
    
    if isinstance(exc, DuplicateKeyError):
        return create_error_response(
            status_code=status.HTTP_409_CONFLICT,
            message="Database integrity error",
            details={"error": "The operation would violate database constraints"},
            error_type="database_integrity_error"
        )
    
    # In development, show more details about the error
    error_message = "Database error occurred"
    error_details = None
    if settings.debug:
        error_message = f"MongoDB error: {str(exc)}"
        error_details = {
            "error_type": type(exc).__name__,
            "suggestion": "Check your MONGODB_URI and MONGODB_DB settings in .env file"
        }
    
    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=error_message,
        details=error_details,
        error_type="database_error"
    )


def handle_generic_error(request: Request, exc: Exception) -> JSONResponse:
    """Handle generic unhandled errors"""
    green_logger.log_error(
        exc,
        {
            "path": str(request.url.path),
            "method": request.method,
            "error_type": type(exc).__name__
        }
    )
    
    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="An unexpected error occurred. Please try again later.",
        error_type="internal_server_error"
    )


def register_error_handlers(app):
    """Register all error handlers with the FastAPI app"""
    app.add_exception_handler(RequestValidationError, handle_validation_error)
    app.add_exception_handler(HTTPException, handle_http_exception)
    app.add_exception_handler(PyMongoError, handle_database_error)
    app.add_exception_handler(Exception, handle_generic_error)
