

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from app.dao.dao import UsersDAO
from app.auth.exceptions import TokenNotFound, UserNotFoundException
from app.dao.dao import ChatDAO, ChatMemberDAO
from app.chat.exceptions import ChatAlreadyExistsException, ChatNotFound
from app.chat.schemas import CreateChat, VerifyChat, AddChatMember, VerifyNickname
from app.dao.models import User
from app.dependencies.auth_dep import get_current_user
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit

router = APIRouter()



@router.post("/create_chat")
async def create_chat(data: VerifyChat,
                      user: User = Depends(get_current_user),
                      session: AsyncSession = Depends(get_session_with_commit)):
    if len(data.title) < 5:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The name of chat must be longer than 5 symbols")
    try:
        if not user:
            raise TokenNotFound
        if await ChatDAO(session).find_one_or_none(VerifyChat(title=data.title)):
            raise ChatAlreadyExistsException
        chat = await ChatDAO(session).add(CreateChat(title=data.title, creator_id=user.id))
        await ChatMemberDAO(session).add(AddChatMember(user_id=user.id, chat_id=chat.id))
        return JSONResponse(status_code=200, content=f"Chat {chat.title} successfully created")
    except HTTPException as he:
        logger.error(f"HTTP Error: {he}")
        return JSONResponse(status_code=he.status_code, content=str(he.detail))

@router.post("/add_to_chat/{nickname}")
async def add_to_chat(nickname: str,
                      title: str,
                      user: User = Depends(get_current_user),
                      session: AsyncSession = Depends(get_session_with_commit)):
    try:
        if not user:
            return TokenNotFound
        chat = await ChatDAO(session).find_one_or_none(CreateChat(title=title, creator_id=user.id))
        if not chat:
            raise ChatNotFound
        user_to_add = await UsersDAO(session).find_one_or_none(VerifyNickname(nickname=nickname))
        if not user_to_add:
            raise UserNotFoundException
        await ChatMemberDAO(session).add(AddChatMember(user_id=user_to_add.id, chat_id=chat.id))
        return JSONResponse(status_code=200, content=f"User {nickname} successfully added to {title}")
    except HTTPException as he:
        logger.error(f"HTTP Error: {he}")
        return JSONResponse(status_code=he.status_code, content=str(he.detail))


@router.get("/find_friends")
async def find_by_symbols(description: str,
                          user: User = Depends(get_current_user),
                        session: AsyncSession = Depends(get_session_without_commit)):
    try:
        if not user:
            raise TokenNotFound
        people = await UsersDAO(session).find_users_by_symbols(description)
        return people
    except HTTPException as he:
        logger.error(f"HTTP Error: {he}")
        return JSONResponse(status_code=he.status_code, content=str(he.detail))


