from app.dao.base import BaseDAO
from app.dao.models import User


class UsersDAO(BaseDAO):
    model = User


