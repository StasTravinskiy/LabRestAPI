import time
from fastapi import Request, HTTPException
import redis.asyncio as redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

RATE_LIMITS = {
    "anonymous": (2, 60),
    "authenticated": (10, 60),
}


async def rate_limit(request: Request, user_id: str | None = None):
    """Логіка 'sliding time window'"""
    identity = user_id or request.client.host

    limit_type = "authenticated" if user_id else "anonymous"

    limit, period = RATE_LIMITS[limit_type]

    key = f"rate_limit:{identity}"

    now = int(time.time())
    window_start = now - period

    await r.zremrangebyscore(key, min=0, max=window_start)

    request_count = await r.zcard(key)

    if request_count >= limit:
        raise HTTPException(status_code=429, detail="Too many requests")

    await r.zadd(key, {str(now): now})

    await r.expire(key, period)