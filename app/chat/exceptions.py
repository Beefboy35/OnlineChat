from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

ChatAlreadyExistsException = JSONResponse(
    status_code=status.HTTP_409_CONFLICT,
    content="Such chat already exists"
)

ChatNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Чат не существует или вы не являетесь его творцом"
)