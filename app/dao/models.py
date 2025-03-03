from datetime import datetime
from typing import List

from sqlalchemy import text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.dao.database import Base, str_uniq




class User(Base):
    phone_number: Mapped[str_uniq]
    nickname: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str_uniq]
    password: Mapped[str]

# class Chat(Base):
#     __tablename__ = "chats"
#     chat_id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str] = mapped_column(nullable=False)
#     chat_type: Mapped[str] = mapped_column(nullable=False)  # 'personal' or 'group'
#
# class Group(Base):
#     __tablename__ = "groups"
#     group_id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str] = mapped_column(nullable=False)
#     creator_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
#     members: Mapped[List[User]] = relationship('User', secondary='group_members')
#
# class Message(Base):
#     __tablename__ = "messages"
#     message_id: Mapped[int] = mapped_column(primary_key=True)
#     chat_id: Mapped[int] = mapped_column(ForeignKey('chats.chat_id'), nullable=False)
#     sender_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), nullable=False)
#     text: Mapped[str] = mapped_column(nullable=False)
#     timestamp: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
#     read: Mapped[bool] = mapped_column(default=False)
#
# class GroupMember(Base):
#     __tablename__ = "group_members"
#     group_id: Mapped[int] = mapped_column(ForeignKey('groups.group_id'), primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
# def __repr__(self):
#     return f"{self.__class__.__name__}(id={self.id})"
