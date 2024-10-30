# Task Manager

Веб-приложение для управления списком задач.

- Создание задачи (POST /tasks)
- Получение списка всех задач (GET /tasks)
- Обновление задачи (PUT /tasks/{id})
- Удаление задачи (DELETE /tasks/{id})
- Регистрация пользователя (POST /auth/register): принимает username и password
- Вход в систему (POST /auth/login): возвращает access и refresh токены
- Обновление access токена (POST /auth/refresh) с использованием refresh токена

СТЕК:
- Python 3.10
- FastApi
- PostgreSQL
- Redis

## Подготовка к установке

Python 3.10 должен быть установлен.Создайте виртуальное окружение и установите зависимости командой:

```pip install -r requirements.txt```

Создайте базы данных PostgreSQL 16 и Redis. В корне проекта создайте
'.env' файл с переменными окружения:

```
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=root
DB_NAME=postgres
ENCRYPTION_KEY=s3XUjyntOk0o=
JWT_SECRET_KEY=asdlajsdasASDASD=
ALGORITHM=HS256
JWT_TOKEN_DELAY_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ORIGINS=["http://127.0.0.1:8000", "http://127.0.0.1:3000"]
REDIS_HOST=localhost
REDIS_PORT=6379
```
где:

- `DB_HOST` адрес БД, по умолчанию 'localhost'
- `DB_PORT` порт БД, по умолчанию '5432'
- `DB_USER` пользователь БД, по умолчанию 'postgres'
- `DB_PASS` пароль БД, по умолчанию 'root'
- `DB_NAME` название БД, по умолчанию 'postgres'
- `ENCRYPTION_KEY` ключ для шифрования паролей пользователей, нет значения по умолчанию
- `JWT_SECRET_KEY` ключ для генерации JWT-токена, нет значения по умолчанию
- `ALGORITHM` алгоритм для шифрования JWT-токена, по умолчанию 'HS256'
- `JWT_TOKEN_DELAY_MINUTES` время жизни JWT-токена в минутах, по умолчанию 30
- `REFRESH_TOKEN_EXPIRE_DAYS` время жизни refresh токена в днях, по умолчанию 7
- `ORIGINS` список разрешенных адресов для работы с API, по умолчанию '["http://127.0.0.1:8000", "http://127.0.0.1:3000"]'
- `REDIS_HOST` адрес redis, по умолчанию 'localhost'
- `REDIS_PORT` порт redis, по умолчанию '6379'

Примените миграции командой:
```sh
$ alembic upgrade head
```