import redis.asyncio as redis
from app.config import Config

JTI_EXPIRY = 60 * 60  # 1 hour

# Create an async Redis client
token_blocklist = redis.Redis(
    host=Config.UPSTASH_REDIS_HOST,
    port=Config.UPSTASH_REDIS_PORT,
    password=Config.UPSTASH_REDIS_PASSWORD,
    ssl=True,
    decode_responses=True
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.setex(
        name=jti,
        time=JTI_EXPIRY,  # Expiry time in seconds
        value=""  # Empty value just to track presence
)

async def token_in_block_list(jti: str) -> bool: 
    return await token_blocklist.exists(jti) > 0  # Check if key exists
