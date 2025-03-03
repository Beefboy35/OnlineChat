import re

from pydantic import BaseModel, ConfigDict,  Field, computed_field



class VerifyModel(BaseModel):
    email: str = Field(description="Электронная почта")
    phone_number: str = Field(description="Номер телефона в международном формате, начинающийся с '+'")
    model_config = ConfigDict(from_attributes=True)



class UserBase(VerifyModel):
    first_name: str = Field(max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(max_length=50, description="Фамилия, от 3 до 50 символов")
    nickname: str = Field(max_length=18, description="Никнейм, от 5 до 18 символов")



class SUserRegister(UserBase):
    password: str = Field(description="Пароль, от 5 до 50 знаков")
    confirm_password: str = Field( description="Повторите пароль")



class SUserAddDB(UserBase):
    password: str = Field(description="Пароль в формате HASH-строки")

class EmailModel(BaseModel):
    email: str

class SUserAuth(EmailModel):
    password: str = Field(description="Пароль, от 8 до 50 знаков")


class RoleModel(BaseModel):
    id: int = Field(description="Идентификатор роли")
    name: str = Field(description="Название роли")
    model_config = ConfigDict(from_attributes=True)


class SUserInfo(UserBase):
    id: int = Field(description="Идентификатор пользователя")

    @computed_field
    def role_name(self) -> str:
        return self.role.name

    @computed_field
    def role_id(self) -> int:
        return self.role.id
