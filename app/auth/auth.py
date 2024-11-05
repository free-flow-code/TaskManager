import base64
import logging
from typing import List
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from cryptography.fernet import Fernet

from app.config import settings
from app.auth.dao import UsersDAO
from app.exceptions import IncorrectUserOrPasswordException


class Settings(BaseModel):
    authjwt_algorithm: str = settings.JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [settings.JWT_ALGORITHM]
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_public_key: str = base64.b64decode(
        settings.JWT_PUBLIC_KEY).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(
        settings.JWT_PRIVATE_KEY).decode('utf-8')


@AuthJWT.load_config
def get_config():
    return Settings()


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
