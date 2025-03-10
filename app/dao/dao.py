from fastapi import HTTPException
from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

from app.auth.exceptions import UserNotFoundException
from app.auth.schemas import UserBase
from app.dao.base import BaseDAO
from app.dao.models import Chat, Message, ChatMember, User


class UsersDAO(BaseDAO):
    model = User
    async def find_users_by_symbols(self, description):
        try:
            stmt = select(User).filter(User.nickname.like(f"%{ description }%"))
            people = await self._session.execute(stmt)
            people = people.scalars().all()
            if not people:
                raise UserNotFoundException
            result = []
            for person in people:
                result.append(UserBase(
                    first_name=person.first_name,
                    last_name=person.last_name,
                    email=person.email,
                    phone_number=person.phone_number,
                    nickname=person.nickname
                ))
            return result
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске всех юзеров по символам {description}: {e}")
            raise


class ChatDAO(BaseDAO):
    model = Chat


class MessageDAO(BaseDAO):
    model = Message


class ChatMemberDAO(BaseDAO):
    model = ChatMember