from app.dao.base import BaseDAO
from app.dao.models import Chat, Message, ChatMember


class ChatDAO(BaseDAO):
    model = Chat


class MessageDAO(BaseDAO):
    model = Message


class ChatMemberDAO(BaseDAO):
    model = ChatMember