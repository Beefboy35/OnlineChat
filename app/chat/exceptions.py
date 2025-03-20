from starlette import status
from starlette.exceptions import HTTPException


ChatAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Such chat already exists"
)

ChatNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Chat doesn't exist or you are not its creator"
)


InvalidChatIdEXception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Choose one of your own chat or create a new one!"
)