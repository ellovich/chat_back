from app.base.dao import BaseDAO
from app.user.model import User
from app.user.schemas import SUserCreate, SUserUpdate


class UserDAO(BaseDAO[User, SUserCreate, SUserUpdate]):
    model = User
