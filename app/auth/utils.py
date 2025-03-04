import re

from email_validator import validate_email, EmailUndeliverableError
from fastapi import Depends
from passlib.context import CryptContext
from authlib.jose import jwt

from fastapi.responses import Response

from app.config import settings

from app.auth.exceptions import InvalidEmailException, InvalidPasswordException, InvalidPhoneNumberException, \
    NamesStartWithCapLetter
from app.dao.models import User
from app.dependencies.auth_dep import check_refresh_token


def create_tokens(data: dict) -> dict:
    access_payload = data.copy()
    headers = {"alg": settings.ALGORITHM}
    access_token = jwt.encode(
        header=headers,
        payload=access_payload,
        key=settings.SECRET_KEY,
    )
    refresh_payload = data.copy()
    headers = {"alg": settings.ALGORITHM}
    refresh_token = jwt.encode(
        header=headers,
        payload=refresh_payload,
        key=settings.SECRET_KEY,
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


async def authenticate_user(user, password):
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user

def is_the_same_password(password: str, conf_password: str):
    return password == conf_password


def validate_credentials(first_name: str, last_name: str, password: str, email: str, phone_number: str):
    if first_name != first_name.capitalize() or last_name != last_name.capitalize():
        raise NamesStartWithCapLetter
    if not validate_password(password):
        raise InvalidPasswordException
    if not validate_phone_number(phone_number):
        raise InvalidPhoneNumberException
    try:
        if not validate_email(email):
            raise InvalidEmailException
    except EmailUndeliverableError:
        raise InvalidEmailException



def set_tokens(response: Response, user_id: int):
    new_tokens = create_tokens(data={"sub": str(user_id)})
    access_token = new_tokens.get('access_token')
    refresh_token = new_tokens.get("refresh_token")
    response.set_cookie(
        key="user_access_token",
        value=access_token.decode("utf-8"),
        httponly=True,
        max_age=settings.ACCESS_TOKEN_ALIVE_TIME * 60,
        secure=True,
        samesite="lax"
    )

    response.set_cookie(
        key="user_refresh_token",
        value=refresh_token.decode("utf-8"),
        httponly=True,
        max_age=settings.REFRESH_TOKEN_ALIVE_TIME * 60,
        secure=True,
        samesite="lax"
    )
    return response
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def validate_password(password: str) -> bool:
    if len(password) < 8 or len(password) > 20:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True

def validate_phone_number(phone: str) -> bool:
    if not re.match(r'^\+\d{5,15}$', phone):
        return False
    return True

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

