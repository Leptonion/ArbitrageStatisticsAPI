from fastapi import Depends
from fastapi_users import IntegerIDMixin, BaseUserManager

from auth.utils import get_user_db
from config import SECRET_AUTH
from database import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
