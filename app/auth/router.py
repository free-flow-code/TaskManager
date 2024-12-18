import logging
from fastapi import APIRouter, Depends, Response, status

from app.auth.schemas import SUserAuth
from app.auth.dao import UsersDAO

from app.exceptions import (
    UserAlreadyExistException,
    UserNotAddedException,
)

from app.auth.auth import (
    get_password_hash,
    validate_auth_user,
    create_access_token,
    create_refresh_token,
    require_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
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
        logging.error(f"{err}")
        raise UserNotAddedException
    return {"message": "Клиент успешно зарегистрирован"}


@router.post("/login")
async def login_user(
        response: Response,
        user: SUserAuth = Depends(validate_auth_user)
):
    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})
    response.set_cookie("access_token", access_token, samesite="lax", httponly=True)
    response.set_cookie("refresh_token", access_token, samesite="lax", httponly=True)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
async def refresh_access_token(
        response: Response,
        user: SUserAuth = Depends(require_user)
):
    access_token = create_access_token({"sub": user.username})
    response.set_cookie("access_token", access_token, samesite="lax", httponly=True)
    return {'access_token': access_token}


@router.post("logout")
async def loguot(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
