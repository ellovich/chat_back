from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy

from app.auth.user_manager import get_user_manager
from app.config import settings
from app.user.model import User

cookie_transport = CookieTransport(cookie_max_age=36000)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=36000)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_admin_user = fastapi_users.current_user(superuser=True)
