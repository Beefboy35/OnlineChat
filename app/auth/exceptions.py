from fastapi import status, HTTPException


# Пользователь уже существует
UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='User already exists'
)

# Пользователь не найден
UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='User not found'
)

# Отсутствует идентификатор пользователя
UserIdNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Отсутствует идентификатор пользователя'
)

InvalidNicknameException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Никнейм должен содержать английские буквы(заглавные и прописные) и хотя бы одну цифру, длина 5-12 символов. Пример: Beefboy123"
)
# Неверная почта
InvalidEmailException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Invalid email format'
)
InvalidPasswordException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Password must be longer than 7 symbols contain at least one digit and one capital letter, e.g: kEyboard123'
)
NamesStartWithCapLetter = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Name and surname must start with a capital letter"
)

PasswordsDoNotMatchException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Passwords do not match, try again"
)

InvalidPhoneNumberException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Phone number must start with "+" (5-15) digits'
)
# Токен истек
TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token has expired'
)

# Некорректный формат токена
InvalidTokenFormatException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Invalid token format'
)


# Токен отсутствует в заголовке
TokenNotFound = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Please update the page or log in repeatedly'
)

# Невалидный JWT токен
NoJwtException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token is not valid'
)

CSRFTokenError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="CSRF error. Please try again later or contact the support"
)

# Не найден ID пользователя
NoUserIdException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User's id not found"
)

# Недостаточно прав
ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Not enough rights'
)

TokenInvalidFormatException = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token format. 'Bearer <token> expected'"
)