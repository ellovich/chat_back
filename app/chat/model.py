from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.database import BaseAlchemyModel, MainModel


class Chat(BaseAlchemyModel):
    __tablename__ = 'chat'

    doctor_id = Column(Integer, ForeignKey('doctor.user_id'))
    doctor = relationship('Doctor', back_populates='chat')

    patient_id = Column(Integer, ForeignKey('patient.user_id'))
    patient = relationship('Patient', back_populates='chat')

    messages = relationship('Message', back_populates='chat')


class Message(BaseAlchemyModel):
    __tablename__ = 'message'

    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    chat_id = Column(Integer, ForeignKey('chat.id'))
    chat = relationship('Chat', back_populates='messages')

    sender_id = Column(Integer, nullable=False)
    sender = relationship('User', foreign_keys=[sender_id], primaryjoin='User.id == Message.sender_id')

    #is_deleted = Column(Boolean, nullable=False)
    is_read = Column(Boolean, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
