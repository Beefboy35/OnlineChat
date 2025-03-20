from pydantic import BaseModel

class VerifyChat(BaseModel):
    title: str

class CreateChat(VerifyChat):
    creator_id: int

class VerifyNickname(BaseModel):
    nickname: str

class AddChatMember(BaseModel):
    user_id: int
    chat_id: int

class VerifyCreator(BaseModel):
    creator_id: int


class UserToAdd(VerifyNickname):
    title: str

