from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger
from starlette.middleware.sessions import SessionMiddleware
from GUI.router import router as gui_router
from app.auth.router import router as router_auth
from app.config import settings
from app.WebSocket.router import router as ws_router

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    """Управление жизненным циклом приложения."""
    logger.info("Инициализация приложения...")
    yield
    logger.info("Завершение работы приложения...")


def create_app() -> FastAPI:
    """
   Создание и конфигурация FastAPI приложения.

   Returns:
       Сконфигурированное приложение FastAPI
   """
    app = FastAPI(
        title="Websocket Chat",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_KEY)
    # Монтирование статических файлов
    app.mount(
        '/GUI/static',
        StaticFiles(directory='GUI/static'),
        name='static'
    )

    # Регистрация роутеров
    register_routers(app)
    return app


def register_routers(app: FastAPI) -> None:
    """Регистрация роутеров приложения."""
    # Корневой роутер
    root_router = APIRouter()
    app.include_router(root_router, tags=["root"])
    app.include_router(router_auth, tags=['Auth'], prefix="/auth")
    app.include_router(gui_router, tags=["GUI"])
    app.include_router(ws_router, tags=["WebSockets"], prefix="/ws")


# Создание экземпляра приложения
app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8011, reload=True)