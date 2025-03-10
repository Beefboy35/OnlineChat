from starlette import status
from starlette.exceptions import HTTPException

ChatAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Such chat already exists"
)

ChatNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Чат не существует или вы не являетесь его творцом"
)