from fastapi import HTTPException, status

UserAlreadyExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует.",
)

UserNotAddedException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Не удалось зарегистрировать пользователя",
)