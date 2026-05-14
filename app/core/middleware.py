from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.rate_limiter import TokenBucket


bucket = TokenBucket(capacity=20, refill_rate=5)  # can be changed later


async def rate_limit_middleware(request: Request, call_next):
    if not bucket.allow_request():
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"}
        )

    return await call_next(request)