import logging

from fastapi import APIRouter

from app.auth.schemas import SUserAuth
from app.auth.dao import UsersDAO
from app.exceptions import UserAlreadyExistException, UserNotAddedException
from app.auth.auth import get_password_hash

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"]
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(username=user_data.username)
    if existing_user:
        raise UserAlreadyExistException

    hashed_password = get_password_hash(user_data.password)
    new_user_data = user_data.dict()
    new_user_data["password_hash"] = hashed_password
    new_user_data.pop("password")

    try:
        await UsersDAO.add(**new_user_data)
    except Exception as err:
        logging.info(f"{err}")
        raise UserNotAddedException
    return {"message": "Клиент успешно зарегистрирован"}
