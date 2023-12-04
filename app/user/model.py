from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import BaseAlchemyModel, MainModel


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

    def __str__(self) -> str:
        return f"U#{self.id}:{self.email}"
    
    type = Column(String)
