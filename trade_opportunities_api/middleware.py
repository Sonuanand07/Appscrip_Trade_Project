from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, HTTPException
import os

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])

# In-memory backend by default if no storage_url

@limiter.limit("10/minute")
async def rate_limit(request: Request):
    pass

# To use in app: app.add_middleware or decorator on endpoint

