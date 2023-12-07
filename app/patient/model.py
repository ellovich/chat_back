from app.database import BaseAlchemyModel, MainModel
from app.user.model import User
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Patient(BaseAlchemyModel, MainModel):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True, nullable=False, index=True, unique=True)

    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
    user = relationship('User', foreign_keys=[user_id], primaryjoin='User.id == Patient.user_id')
    chat = relationship("Chat", back_populates=__tablename__)
   
    gender: Mapped[String] = mapped_column(String(1), nullable=True)    
    birth_date: Mapped[Date] = mapped_column(Date, nullable=True)    

    def __str__(self) -> str:
        return f"P#{self.id}"
