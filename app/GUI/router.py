import secrets

from fastapi import APIRouter, Depends
from loguru import logger

from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, Response
from starlette.templating import Jinja2Templates

from app.auth.utils import set_tokens, create_tokens
from app.config import settings
from app.dao.models import User
from app.auth.schemas import SUserInfo
from app.dependencies.auth_dep import get_current_user, check_refresh_token, get_refresh_token
from app.dependencies.dao_dep import get_session_without_commit

templates = Jinja2Templates(directory='GUI/templates')
router = APIRouter()
@router.get("/", response_class=HTMLResponse)
async def register_page(request: Request):
    token = secrets.token_hex(32)
    # сохраняем CSRF токен в сессии
    request.session["csrf_token"] = token
    return templates.TemplateResponse("register.html", {"request": request, "csrf_token": token})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    # получаем CSRF токен из сессии
    token = request.session.get("csrf_token")
    return templates.TemplateResponse("login.html", {"request": request,"csrf_token": token})

@router.get("/main_page", response_class=HTMLResponse)
async def main_page(
                    request: Request,
                    user_data: User | None = Depends(get_current_user),
                    refresh_data: User | None = Depends(check_refresh_token)
                    ):
    if not user_data:
        user_data = refresh_data
        if not user_data:
            return RedirectResponse("/login")
    user = SUserInfo.model_validate(user_data)
    return templates.TemplateResponse("main_page.html", {
        "request": request,
        "nickname": user.nickname,
        "phone": user.phone_number,
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
    })