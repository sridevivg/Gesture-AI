"""Redis asynchronous client connection management."""

from typing import Optional
import redis.asyncio as aioredis
from app.core.config import settings

redis_client: Optional[aioredis.Redis] = None


async def get_redis_client() -> aioredis.Redis:
    """Return singleton Redis connection instance."""
    global redis_client
    if redis_client is None:
        redis_client = aioredis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            health_check_interval=30,
        )
    return redis_client


async def close_redis_client() -> None:
    """Close connection pool gracefully."""
    global redis_client
    if redis_client is not None:
        await redis_client.close()
        redis_client = None
