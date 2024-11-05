from fastapi import HTTPException, status

UserAlreadyExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует.",
)

UserNotAddedException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Не удалось зарегистрировать пользователя.",
)

IncorrectUserOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверное имя пользователя или пароль.",
)

IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Не верный формат токена.'
)

UserNotExistException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Пользователь принадлежащий этому токену не зарегистрирован.'
)

TokenNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен не найден."
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истек.",
)
