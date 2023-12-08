from typing import AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from app.database import async_session_maker
from app.user.model import AccessToken, User


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_access_token_db(session: AsyncSession = Depends(get_async_session)):  
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
