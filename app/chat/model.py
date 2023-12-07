from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.database import BaseAlchemyModel, MainModel


class Chat(BaseAlchemyModel):
    __tablename__ = 'chat'

    doctor_user_id = Column(Integer, ForeignKey('doctor.user_id'))
    doctor = relationship('Doctor', back_populates='chat')

    patient_user_id = Column(Integer, ForeignKey('patient.user_id'))
    patient = relationship('Patient', back_populates='chat')

    messages = relationship('Message', back_populates='chat')


class Message(BaseAlchemyModel):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, nullable=False)

    chat_id = Column(Integer, ForeignKey('chat.id'))
    chat = relationship('Chat', back_populates='messages')

    sender_id = Column(Integer, nullable=False)
    sender = relationship('User', foreign_keys=[sender_id], primaryjoin='User.id == Message.sender_id')

    attachments = relationship('Attachment', back_populates='message')

    def as_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp,
            'is_read': self.is_read,
            'sender_id': self.sender_id,
            'attachments': [attachment.file_path for attachment in self.attachments]
        }
    

class Attachment(BaseAlchemyModel):
    __tablename__ = 'attachment'

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    message_id = Column(Integer, ForeignKey('message.id'))
    message = relationship('Message', back_populates='attachments')

