from jose import jwt
from datetime import datetime, timedelta

from app.config import settings
from app.auth.schemas import SUserAuth


def create_jwt(user: SUserAuth, token_type: str, expire: int) -> str:
    jwt_payload = {
        "type": token_type,
        "sub": user.username,
        "username": user.username,
        "exp": expire
    }
    return jwt.encode(
        jwt_payload, settings.JWT_SECRET_KEY, settings.ALGORITHM
    )


def create_access_token(user: SUserAuth) -> str:
    expire = (datetime.utcnow() + timedelta(minutes=settings.JWT_TOKEN_DELAY_MINUTES)).timestamp()
    return create_jwt(user, "access", int(expire))


def create_refresh_token(user: SUserAuth) -> str:
    expire = (datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)).timestamp()
    return create_jwt(user, "refresh", int(expire))
