from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyBaseAccessTokenTable,
)
from app.database import BaseAlchemyModel, MainModel


class AccessToken(SQLAlchemyBaseAccessTokenTable[int], BaseAlchemyModel):
    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False)
    user = relationship('User', back_populates='access_tokens')

    def __str__(self) -> str:
        return f"T#{self.user_id}: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class User(BaseAlchemyModel, MainModel):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False, index=True, unique=True)

    email = Column(String(length=100), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    phone_number = Column(String, default=False, nullable=True)

    image_path = Column(String, nullable=True)
    
    type = Column(String)

    access_tokens = relationship('AccessToken', back_populates='user')

    def __str__(self) -> str:
        return f"U#{self.id}:{self.email}"
