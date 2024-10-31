import logging
from cryptography.fernet import Fernet

from app.config import settings
from app.auth.dao import UsersDAO
from app.exceptions import IncorrectUserOrPasswordException

key = settings.ENCRYPTION_KEY
cipher_suite = Fernet(key)


def get_password_hash(password: str) -> str:
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password.decode()


def get_password_from_hash(encrypted_password: str) -> str:
    decrypted_password = cipher_suite.decrypt(encrypted_password.encode())
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
