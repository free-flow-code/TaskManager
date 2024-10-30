from sqlalchemy import Column, Integer, String

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)

    def __str__(self):
        return f"Пользователь {self.username}"
