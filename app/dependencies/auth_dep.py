import secrets

from authlib.jose.errors import InvalidTokenError
from fastapi import Request, Depends
from authlib.jose import jwt
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dao import UsersDAO
from app.dao.models import User
from app.config import settings
from app.dependencies.dao_dep import get_session_without_commit
from app.auth.exceptions import (
    NoJwtException, TokenExpiredException, NoUserIdException, UserNotFoundException, TokenNotFound
)


def get_access_token(request: Request) -> str | None:
    """Извлекаем access_token из кук."""
    token = request.cookies.get('user_access_token')
    if not token:
        return None
    return token


def get_refresh_token(request: Request) -> str | None:
    """Извлекаем refresh_token из кук."""
    token = request.cookies.get('user_refresh_token')
    if not token:
        return None
    return token


async def check_refresh_token(
        token: str = Depends(get_refresh_token),
        session: AsyncSession = Depends(get_session_without_commit)
) -> User | None:
    """ Проверяем refresh_token и возвращаем пользователя."""
    if not token:
        raise TokenExpiredException
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
        )
        user_id = payload.get("sub")
        if not user_id:
            raise NoJwtException

        user = await UsersDAO(session).find_one_or_none_by_id(data_id=int(user_id))
        if not user:
            raise NoJwtException

        return user
    except InvalidTokenError:
        raise NoJwtException

def is_valid_csrf_token(request: Request, token: str) -> bool:
    stored_token = request.session.get("csrf_token")
    if not token:
        return False
    return secrets.compare_digest(stored_token, token) if stored_token else False

async def get_current_user(
        token: str = Depends(get_access_token),
        session: AsyncSession = Depends(get_session_without_commit)
) -> User | None:
    """Проверяем access_token и возвращаем пользователя."""
    if not token:
        return TokenNotFound
    try:
        # Декодируем токен
        payload = jwt.decode(token, settings.SECRET_KEY)
    except InvalidTokenError:
        # Общая ошибка для токенов
        raise NoJwtException

    user_id: str = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    user = await UsersDAO(session).find_one_or_none_by_id(data_id=int(user_id))
    if not user:
        raise UserNotFoundException
    return user
