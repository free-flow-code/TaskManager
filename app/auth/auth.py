import logging
from pytz import timezone
from fastapi import Request
from jose import jwt, JWTError
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

from app.config import settings
from app.auth.dao import UsersDAO

from app.exceptions import (
    IncorrectUserOrPasswordException,
    TokenNotFoundException,
    IncorrectTokenFormatException,
    UserNotExistException,
    TokenExpiredException,
)

CIFER_SUITE = Fernet(settings.ENCRYPTION_KEY)


def get_password_hash(password: str) -> str:
    encrypted_password = CIFER_SUITE.encrypt(password.encode())
    return encrypted_password.decode()


def get_password_from_hash(encrypted_password: str) -> str:
    decrypted_password = CIFER_SUITE.decrypt(encrypted_password.encode())
    return decrypted_password.decode()


def verify_password(plain_password: str, password_hash: str) -> bool:
    try:
        decrypted_password = get_password_from_hash(password_hash)
        return plain_password == decrypted_password
    except Exception as err:
        logging.info(f"Ошибка при расшифровке пароля {err}")
        return False


async def validate_auth_user(username: str, password: str):
    user = await UsersDAO.find_one_or_none(username=username)

    if not user:
        raise IncorrectUserOrPasswordException
    if not verify_password(password, user.password_hash):
        raise IncorrectUserOrPasswordException
    return user


def create_token(data: dict, expire: float) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_access_token(data: dict):
    current_time = datetime.now(timezone(settings.SERVER_TIMEZONE))
    expire = current_time + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_token(data, expire.timestamp())


def create_refresh_token(data: dict):
    current_time = datetime.now(timezone(settings.SERVER_TIMEZONE))
    expire = current_time + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return create_token(data, expire.timestamp())


async def require_user(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise TokenNotFoundException

    try:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get("exp")
    current_time = datetime.now(timezone(settings.SERVER_TIMEZONE))
    if (not expire) or (float(expire) < current_time.timestamp()):
        raise TokenExpiredException

    username: str = payload.get("sub")
    if not username:
        raise IncorrectTokenFormatException

    user = await UsersDAO.find_one_or_none(username=username)
    if not user:
        raise UserNotExistException

    return user
