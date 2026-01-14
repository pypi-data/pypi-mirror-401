"""Authentication middleware for gateway endpoints."""

from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from app.config import get_settings

security = HTTPBearer(auto_error=False)


class TokenPayload(BaseModel):
    """JWT token payload."""

    sub: str  # user ID
    exp: datetime
    iat: datetime
    org_id: str | None = None


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> TokenPayload | None:
    """
    Validate JWT token and return user info.

    Returns None if no token provided (for public endpoints).
    Raises 401 if token is invalid.
    """
    if credentials is None:
        return None

    settings = get_settings()

    try:
        # Supabase JWTs need audience verification disabled
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            options={"verify_aud": False},
        )
        return TokenPayload(
            sub=payload.get("sub", ""),
            exp=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
            iat=datetime.fromtimestamp(payload["iat"], tz=timezone.utc),
            org_id=payload.get("org_id"),
        )
    except JWTError as e:
        import logging
        logging.error(f"JWT verification failed: {e}, secret_len={len(settings.jwt_secret)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def require_auth(
    user: Annotated[TokenPayload | None, Depends(get_current_user)],
) -> TokenPayload:
    """Require authentication - raises 401 if not authenticated."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
