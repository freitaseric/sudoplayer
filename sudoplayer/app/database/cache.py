from datetime import datetime
import redis.asyncio as redis

from sudoplayer.core import env


cache = redis.Redis(
    host=env.REDIS_HOST,
    port=env.REDIS_PORT,
    username=env.REDIS_USERNAME,
    password=env.REDIS_PASSWORD,
    decode_responses=True,
)


async def get_created_at(key: str) -> datetime:
    created_at_str = await cache.get(f"{key}:created_at")

    return datetime.fromisoformat(created_at_str)
