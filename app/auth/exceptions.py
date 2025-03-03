from fastapi import status, HTTPException

# Пользователь уже существует
UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь уже существует'
)

# Пользователь не найден
UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Пользователь не найден'
)

# Отсутствует идентификатор пользователя
UserIdNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Отсутствует идентификатор пользователя'
)

# Неверная почта
InvalidEmailException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Неверный формат почты'
)
InvalidPasswordException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Пароль должен содержать не менее 8 символов(английские буквы) и не более 20, иметь хотя бы одну цифру и заглавную букву. Пример: kEyboard123'
)

PasswordsDoNotMatchException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Пароли не совпадают, попробуйте еще раз"
)

InvalidPhoneNumberException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр'
)
# Токен истек
TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен истек'
)

# Некорректный формат токена
InvalidTokenFormatException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Некорректный формат токена'
)


# Токен отсутствует в заголовке
TokenNotFound = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Токен отсутствует в заголовке'
)

# Невалидный JWT токен
NoJwtException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен не валидный'
)

CSRFTokenError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="CSRF ошибка. Пожалуйста попробуйте позже или свяжитесь с поддержкой"
)

# Не найден ID пользователя
NoUserIdException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Не найден ID пользователя'
)

# Недостаточно прав
ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Недостаточно прав'
)

TokenInvalidFormatException = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный формат токена. Ожидается 'Bearer <токен>'"
)