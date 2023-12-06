from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase

from app.config import settings
from app.doctor.dao import DoctorDAO
from app.logger import logger
from app.patient.dao import PatientDAO
from app.user.dependencies import get_user_db
from app.user.model import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        logger.info(f"User {user.id} has logged in.")

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        if user.type == "patient":
            await PatientDAO.add(user_id=user.id, attribs=[])
        elif user.type == "doctor":
            await DoctorDAO.add(user_id=user.id, education=[])
        logger.info(f"User {user.id} ({user.type}) has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"Verification requested for user {user.id}. Verification token: {token}")

    async def on_after_verify(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        logger.info(f"User {user.id} has been verified.")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
