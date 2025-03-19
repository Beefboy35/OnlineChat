import os
import warnings

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:1234@localhost:5432/test_chat"
    SECRET_KEY: str = "changethis"
    SESSION_KEY: str = "changethis"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_ALIVE_TIME: int = 30
    REFRESH_TOKEN_ALIVE_TIME: int = 2880
    BASE_URL: str = "http://localhost:8011"
    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"


    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))


    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)
# Получаем параметры для загрузки переменных среды
settings = Settings()
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
logger.add(sink=log_file_path, format=settings.FORMAT_LOG, level="INFO")
database_url = settings.DB_URL
