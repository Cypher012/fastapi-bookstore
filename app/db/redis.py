import aioredis
from app.config import Config

JTI_EXPIRY = 60 * 60

token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value = "",
        expire=JTI_EXPIRY,
    )

async def token_in_block_list(jti: str) -> bool: 
    jti = await token_blocklist.get(jti)

    return jti is not None