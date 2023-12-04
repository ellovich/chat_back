from app.database import BaseAlchemyModel, MainModel
from app.user.model import User
from sqlalchemy import ARRAY, JSON, Boolean, Column, Computed, Date, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Patient(BaseAlchemyModel, MainModel):
    __tablename__ = "patient"
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
    user = relationship('User', foreign_keys=[user_id], primaryjoin='User.id == Patient.user_id')
    chat = relationship("Chat", back_populates=__tablename__)
   
    gender: Mapped[String] = mapped_column(String(1), nullable=True)    
    attribs: Mapped[JSONB] = mapped_column(JSONB, nullable=False)

    def __str__(self) -> str:
        return f"P#{self.id}"
    