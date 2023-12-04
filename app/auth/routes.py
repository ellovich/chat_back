from fastapi import APIRouter, Depends, FastAPI

from app.auth.auth import auth_backend, current_active_user, current_admin_user, fastapi_users
from app.user.model import User
from app.user.schemas import SUserCreate, SUserRead, SUserUpdate


def add_auth_routes(app: FastAPI):
    app.include_router(
        fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["Auth"]
    )
    app.include_router(
        fastapi_users.get_register_router(SUserRead, SUserCreate),
        prefix="/auth",
        tags=["Auth"],
    )
    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["Auth"],
    )
    app.include_router(
        fastapi_users.get_verify_router(SUserRead),
        prefix="/auth",
        tags=["Auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(SUserRead, SUserUpdate),
        prefix="/users",
        tags=["Auth"],
    )
