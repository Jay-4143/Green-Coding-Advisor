"""
Shared rate limiter instance for use across routers.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

from .config import settings

# Use a generous limit to avoid test flakiness; adjust if needed for prod
limit_per_minute = "1000/minute" if settings.environment.lower() != "production" else f"{settings.rate_limit_per_minute}/minute"

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[limit_per_minute],
)

