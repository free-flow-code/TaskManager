from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore"
    )
    SERVER_TIMEZONE: str = "Europe/Moscow"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "root"
    DB_NAME: str = "mydb"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ENCRYPTION_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_PRIVATE_KEY: str = None
    JWT_PUBLIC_KEY: str = None
    ORIGINS: list = ["localhost:8000", "127.0.0.1:8000"]


settings = Settings()
