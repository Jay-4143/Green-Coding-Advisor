"""
Security utilities for input validation, sanitization, and security headers.
"""
import re
import html
from typing import Any, Dict, List, Optional
from fastapi import Request, Response
from fastapi.responses import JSONResponse


def sanitize_string(value: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize a string input by:
    - Escaping HTML entities
    - Removing null bytes
    - Truncating to max_length if provided
    """
    if not isinstance(value, str):
        return str(value)
    
    # Remove null bytes
    sanitized = value.replace('\x00', '')
    
    # Escape HTML entities
    sanitized = html.escape(sanitized)
    
    # Truncate if max_length provided
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_username(username: str) -> bool:
    """Validate username format (alphanumeric, underscore, hyphen, 3-30 chars)"""
    pattern = r'^[a-zA-Z0-9_-]{3,30}$'
    return bool(re.match(pattern, username))


def sanitize_code_content(code: str, max_length: int = 100000) -> str:
    """
    Sanitize code content:
    - Remove null bytes
    - Truncate if too long
    - Basic validation
    """
    if not isinstance(code, str):
        raise ValueError("Code content must be a string")
    
    # Remove null bytes
    sanitized = code.replace('\x00', '')
    
    # Check length
    if len(sanitized) > max_length:
        raise ValueError(f"Code content exceeds maximum length of {max_length} characters")
    
    return sanitized


def validate_language(language: str) -> bool:
    """Validate programming language"""
    allowed_languages = ['python', 'java', 'javascript', 'typescript', 'cpp', 'c']
    return language.lower() in allowed_languages


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and other attacks
    """
    if not isinstance(filename, str):
        raise ValueError("Filename must be a string")
    
    # Remove path separators
    sanitized = filename.replace('/', '').replace('\\', '').replace('..', '')
    
    # Remove null bytes
    sanitized = sanitized.replace('\x00', '')
    
    # Limit length
    if len(sanitized) > 255:
        sanitized = sanitized[:255]
    
    return sanitized


def add_security_headers(response: Response) -> Response:
    """
    Add security headers to response
    """
    # Prevent clickjacking
    response.headers["X-Frame-Options"] = "DENY"
    
    # Prevent MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    
    # XSS Protection
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # Referrer Policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Content Security Policy (adjust based on your needs)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self' https:;"
    )
    
    # Permissions Policy
    response.headers["Permissions-Policy"] = (
        "geolocation=(), "
        "microphone=(), "
        "camera=(), "
        "payment=(), "
        "usb=()"
    )
    
    # Strict Transport Security (only in production with HTTPS)
    # response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response


async def security_middleware(request: Request, call_next):
    """
    Middleware to add security headers to all responses
    """
    response = await call_next(request)
    return add_security_headers(response)


def validate_pagination_params(skip: int = 0, limit: int = 10) -> tuple[int, int]:
    """
    Validate and sanitize pagination parameters
    """
    # Ensure skip is non-negative
    skip = max(0, skip)
    
    # Ensure limit is between 1 and 100
    limit = max(1, min(100, limit))
    
    return skip, limit

