import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

logging.basicConfig(
        level=logging.DEBUG,
        filename='main_app_log.log',
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s'
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Service started")
    yield
    logging.info("Service exited")

main_app = FastAPI(
    title="TaskManager",
    openapi_prefix="/api",
    lifespan=lifespan,
    )

origins = settings.ORIGINS

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization"],
)
