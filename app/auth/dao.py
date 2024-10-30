from app.dao.base import BaseDAO
from app.auth.models import Users


class UsersDAO(BaseDAO):
    model = Users
