from cryptography.fernet import Fernet

from app.config import settings

key = settings.ENCRYPTION_KEY
cipher_suite = Fernet(key)


def get_password_hash(password: str) -> str:
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password.decode()
