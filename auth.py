from fastapi import Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_secret_key: str = "your-secret-key-change-in-prod"
    api_key_header: str = "Bearer"

    class Config:
        env_file = ".env"

settings = Settings()

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Simple auth: validate API key in Authorization header.
    User is 'guest' if key present (non-empty).
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # In prod, validate against registered keys or JWT verify
    # For now, accept any non-empty as guest
    user_id = f"guest_{hash(credentials.credentials) % 10000}"  # Simple session-like ID
    return user_id

