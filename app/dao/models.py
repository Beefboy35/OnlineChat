
from typing import List

from sqlalchemy import  ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.dao.database import Base, str_uniq




class User(Base):
    phone_number: Mapped[str_uniq]
    nickname: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str_uniq]
    password: Mapped[str]
    chats = relationship('Chat', secondary='chat_members', back_populates='members')

class Chat(Base):
    title: Mapped[str_uniq] = mapped_column(nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    members = relationship('User', secondary='chat_members', back_populates='chats')

class Message(Base):
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id'), nullable=False)
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    read: Mapped[bool] = mapped_column(default=False)

class ChatMember(Base):
    __tablename__ = "chat_members"
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id'), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
