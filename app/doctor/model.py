from app.database import BaseAlchemyModel, MainModel
from app.user.model import User
from app.chat.model import Chat
from sqlalchemy import JSON, Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship



class Doctor(BaseAlchemyModel, MainModel):
    __tablename__ = "doctor"
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
    user = relationship('User', foreign_keys=[user_id], primaryjoin='User.id == Doctor.user_id')
    chat = relationship("Chat", back_populates=__tablename__)
    
    first_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    @property
    def full_name(self):
        if self.last_name and self.first_name:
            return f"{self.last_name}  {self.first_name} {self.middle_name if self.middle_name else ''}"
        else:
            return f"Doctor {id}"

    @property
    def short_name(self):
        if self.last_name and self.first_name and self.middle_name:
            return f"{self.last_name}  {self.first_name[:1]}. {(self.middle_name[:1]) + '.' if self.middle_name else ''}"
        else:
            return f"Doctor {id}"

    gender = Column(String, nullable=True)
    birth = Column(Date, nullable=True)

    medical_institution = Column(String, nullable=True)
    jobTitle = Column(String, nullable=True)
    education = Column(JSONB, nullable=False)
    career = Column(JSONB, nullable=True)


    def __str__(self) -> str:
        return f"D#{self.id}:{self.short_name}"
