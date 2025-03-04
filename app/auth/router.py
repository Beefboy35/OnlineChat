from typing import List
from fastapi import APIRouter, Response, Depends, HTTPException
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.dao.models import User
from app.auth.utils import authenticate_user, set_tokens, validate_credentials, get_password_hash, is_the_same_password
from app.dependencies.auth_dep import get_current_user, check_refresh_token, is_valid_csrf_token
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from app.auth.exceptions import UserAlreadyExistsException, CSRFTokenError, UserNotFoundException, \
    PasswordsDoNotMatchException
from app.auth.dao import UsersDAO
from app.auth.schemas import SUserRegister, SUserAuth, SUserAddDB, SUserInfo, VerifyModel, EmailModel

router = APIRouter()


@router.post("/register")
async def register_user(response: Response,
                        req: Request,
                        user_data: SUserRegister,
                        session: AsyncSession = Depends(get_session_with_commit),
                        ):
    # Начинаем транзакцию
    async with session.begin():
        try:
            csrf_token = req.headers.get("CSRF-Token")
            if not (csrf_token or is_valid_csrf_token(req, csrf_token)):
                raise CSRFTokenError
            if not is_the_same_password(user_data.password, user_data.confirm_password):
                raise PasswordsDoNotMatchException
            validate_credentials(user_data.first_name, user_data.last_name,
                                 user_data.password, user_data.email, user_data.phone_number)
            user_dao = UsersDAO(session)
            existing_user = await user_dao.find_one_or_none(filters=VerifyModel(
                email=user_data.email,
                phone_number=user_data.phone_number)
            )
            if existing_user:
                raise UserAlreadyExistsException

            user_data.password = get_password_hash(user_data.password)
            user_data_dict = user_data.model_dump()
            user_data_dict.pop('confirm_password', None)
            added_user = await user_dao.add(values=SUserAddDB(**user_data_dict))
            # возращаем сообщение об успехе и устанавливаем JWT токены
            return JSONResponse(status_code=200, content={'message': 'Вы успешно зарегистрированы!'}), set_tokens(response, added_user.id)
        except IntegrityError as ie:
            await session.rollback()  # Откат транзакции
            logger.error(f"Ошибка интеграции с базой данных, откат транзакции: {ie}")
            return JSONResponse(status_code=409, content="Пользователь уже существует")
        except HTTPException as he:
            logger.error(f"HTTP Error: {he}")
            return JSONResponse(status_code=he.status_code, content=str(he.detail))


@router.post("/login")
async def auth_user(
        response: Response,
        req: Request,
        user_data: SUserAuth,
        session: AsyncSession = Depends(get_session_without_commit)
):
    csrf_token = req.headers.get("CSRF-Token")
    if not is_valid_csrf_token(req, csrf_token):
        raise CSRFTokenError
    users_dao = UsersDAO(session)
    user = await users_dao.find_one_or_none(
        filters=EmailModel(email=user_data.email)
    )
    if not (user and await authenticate_user(user=user, password=user_data.password)):
        raise UserNotFoundException
    try:

        return JSONResponse(
            status_code=200,
            content={
                'ok': True,
                'message': 'Авторизация успешна!'
            }), set_tokens(response, user.id)
    except HTTPException as he:
        logger.error(f"HTTP Error: {he}")
        return JSONResponse(status_code=he.status_code, content=str(he.detail))


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("user_access_token")
    response.delete_cookie("user_refresh_token")
    return {'message': 'Пользователь успешно вышел из системы'}


@router.get("/me")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.get("/all_users/")
async def get_all_users(session: AsyncSession = Depends(get_session_with_commit)
                        ) -> List[SUserInfo]:
    return await UsersDAO(session).find_all()


@router.post("/refresh")
async def process_refresh_token(
        response: Response,
        user: User = Depends(check_refresh_token)
):
    set_tokens(response, user.id)
