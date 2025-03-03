import os

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:1234@localhost:5432/postgres"
    SECRET_KEY: str
    SESSION_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_ALIVE_TIME: int
    REFRESH_TOKEN_ALIVE_TIME: int
    BASE_URL: str
    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"


    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))


# Получаем параметры для загрузки переменных среды
settings = Settings()
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
logger.add(sink=log_file_path, format=settings.FORMAT_LOG, level="INFO")
database_url = settings.DB_URL
