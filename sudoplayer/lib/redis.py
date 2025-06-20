import redis.asyncio as redis

from sudoplayer.config import env

r = redis.Redis(
    host=env.REDIS_HOST,
    port=env.REDIS_PORT,
    username=env.REDIS_USERNAME,
    password=env.REDIS_PASSWORD,
    decode_responses=True,
)
