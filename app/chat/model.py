from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.database import BaseAlchemyModel, MainModel


class Chat(BaseAlchemyModel):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True, nullable=False, index=True, unique=True)

    user1_id = Column(Integer, ForeignKey('user.id'))
    user1 = relationship('User', foreign_keys=[user1_id])

    user2_id = Column(Integer, ForeignKey('user.id'))
    user2 = relationship('User', foreign_keys=[user2_id])

    messages = relationship('Message', back_populates='chat', cascade='all, delete-orphan')

    def __str__(self) -> str:
        return f"C#{self.id}<(u#{self.user1_id}<->u#{self.user2_id})>"


class Message(BaseAlchemyModel):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, nullable=False, index=True, unique=True)

    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, nullable=False)

    chat_id = Column(Integer, ForeignKey('chat.id'))
    chat = relationship('Chat', back_populates='messages')

    sender_id = Column(Integer, nullable=False)
    sender = relationship('User', foreign_keys=[sender_id], primaryjoin='User.id == Message.sender_id')

    attachments = relationship('Attachment', back_populates='message', cascade='all, delete-orphan')

    def as_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp,
            'is_read': self.is_read,
            'sender_id': self.sender_id,
            'attachments': [attachment.file_path for attachment in self.attachments]
        }
    
    def __str__(self) -> str:
        return f"M#{self.id}<(u#{self.sender_id})>"
    

class Attachment(BaseAlchemyModel):
    __tablename__ = 'attachment'
    id = Column(Integer, primary_key=True, nullable=False, index=True, unique=True)

    file_path = Column(String, nullable=False)
    message_id = Column(Integer, ForeignKey('message.id'))
    message = relationship('Message', back_populates='attachments')

    type = Column(String, nullable=False, default="image")

