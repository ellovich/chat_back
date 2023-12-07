from datetime import date
import json
from fastapi import HTTPException

from sqlalchemy import and_, desc, func, insert, or_, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, selectinload

from app.base.dao import BaseDAO
from app.chat.model import Chat
from app.chat.schemas import SChatCreate, SChatForList, SChatUpdate, SMessage, SChat, SMessageCreate, SMessageUpdate
from app.database import async_session_maker, engine
from app.logger import logger
from app.chat.model import Message


class ChatDAO(BaseDAO[Chat, SChatCreate, SChatUpdate]):
    model = Chat

    @classmethod
    async def get_chats_by_user(cls, user_id: int) :#-> list[SChatForList]:
        # Подзапрос для получения максимального timestamp для каждого чата
        subquery = (
            select(Message.chat_id, func.max(Message.timestamp).label("max_timestamp"))
            .group_by(Message.chat_id)
            .alias("subquery")
        )

        # Основной запрос для получения чатов пользователя с последними сообщениями
        query = (
            select(Chat, Message.content, Message.timestamp, Message.is_read)
            .join(subquery, Chat.id == subquery.c.chat_id)
            .outerjoin(Message, and_(Chat.id == Message.chat_id, Message.timestamp == subquery.c.max_timestamp))
            .filter(or_(Chat.doctor_user_id == user_id, Chat.patient_user_id == user_id))
            .order_by(desc(subquery.c.max_timestamp))
        )

        async with async_session_maker() as session:
            result = await session.execute(query)
            chats_with_messages = result.scalars().all()

        # Преобразование результатов в список словарей
        chat_list = [
            {
                "chat_id": chat.id,
                "doctor_id": chat.doctor_user_id,
                "patient_id": chat.patient_user_id,
                "last_message": {
                    "id": message.id if message else None,
                    "content": message.content if message else None,
                    "timestamp": message.timestamp if message else None,
                    "sender_id": message.sender_id if message else None,
                    "is_read": message.is_read if message else None,
                },
            }
            for chat, message in chats_with_messages
        ]

        return chat_list or []  # Вернем пустой список, если чаты не найдены


class MessageDAO(BaseDAO[Message, SMessageCreate, SMessageUpdate]):
    model = Message
