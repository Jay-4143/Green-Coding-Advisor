"""
Redis caching utilities for frequently accessed data.
"""
from typing import Optional, Any, Union
import json
try:
    import redis.asyncio as redis
except ImportError:
    redis = None
from .config import settings
from .logger import green_logger

_redis_client: Optional[redis.Redis] = None


async def get_redis_client() -> Optional[Any]:
    """
    Get Redis client instance.
    Returns None if Redis is not configured or unavailable.
    """
    global _redis_client
    
    if redis is None:
        return None
    
    if not settings.redis_url or settings.redis_url == "redis://localhost:6379/0":
        # Redis not configured, return None
        return None
    
    if _redis_client is None:
        try:
            _redis_client = redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=5
            )
            # Test connection
            await _redis_client.ping()
            green_logger.logger.info("Redis connection established")
        except Exception as e:
            green_logger.logger.warning(f"Redis connection failed: {e}. Caching disabled.")
            _redis_client = None
    
    return _redis_client


async def get_cache(key: str) -> Optional[Any]:
    """
    Get value from cache.
    Returns None if not found or Redis unavailable.
    """
    client = await get_redis_client()
    if not client:
        return None
    
    try:
        value = await client.get(key)
        if value:
            return json.loads(value)
    except Exception as e:
        green_logger.logger.warning(f"Cache get error for key {key}: {e}")
    
    return None


async def set_cache(key: str, value: Any, ttl: int = 3600) -> bool:
    """
    Set value in cache with TTL (time to live in seconds).
    Returns True if successful, False otherwise.
    """
    client = await get_redis_client()
    if not client:
        return False
    
    try:
        await client.setex(key, ttl, json.dumps(value))
        return True
    except Exception as e:
        green_logger.logger.warning(f"Cache set error for key {key}: {e}")
        return False


async def delete_cache(key: str) -> bool:
    """
    Delete key from cache.
    Returns True if successful, False otherwise.
    """
    client = await get_redis_client()
    if not client:
        return False
    
    try:
        await client.delete(key)
        return True
    except Exception as e:
        green_logger.logger.warning(f"Cache delete error for key {key}: {e}")
        return False


async def clear_cache_pattern(pattern: str) -> int:
    """
    Clear all cache keys matching pattern.
    Returns number of keys deleted.
    """
    client = await get_redis_client()
    if not client:
        return 0
    
    try:
        keys = await client.keys(pattern)
        if keys:
            return await client.delete(*keys)
        return 0
    except Exception as e:
        green_logger.logger.warning(f"Cache clear pattern error for {pattern}: {e}")
        return 0


def cache_key_user_metrics(user_id: int) -> str:
    """Generate cache key for user metrics"""
    return f"user:metrics:{user_id}"


def cache_key_leaderboard(timeframe: str) -> str:
    """Generate cache key for leaderboard"""
    return f"leaderboard:{timeframe}"


def cache_key_user_badges(user_id: int) -> str:
    """Generate cache key for user badges"""
    return f"user:badges:{user_id}"


def cache_key_submission(submission_id: int) -> str:
    """Generate cache key for submission"""
    return f"submission:{submission_id}"

