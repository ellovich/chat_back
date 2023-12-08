from datetime import date
import json
from fastapi import HTTPException

from sqlalchemy import and_, desc, func, insert, or_, select, update, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, selectinload

from app.base.dao import BaseDAO
from app.chat.model import Chat
from app.chat.schemas import SChatCreate, SChatForList, SChatUpdate, SMessage, SChat, SMessageCreate, SMessageUpdate
from app.database import async_session_maker, engine
from app.logger import logger
from app.chat.model import Message
from app.user.model import User


class ChatDAO(BaseDAO[Chat, SChatCreate, SChatUpdate]):
    model = Chat

    @classmethod
    async def get_chats_list_by_user_id(cls, user_id: int) -> list[SChatForList]:
        async with async_session_maker() as session:
            # Получим чаты, где текущий пользователь является user1 или user2
            stmt = select(Chat).filter((Chat.user1_id == user_id) | (Chat.user2_id == user_id))
            result = await session.execute(stmt)
            user_chats = result.scalars().all()

            chat_list = []
            for chat in user_chats:
                # Определите user_id собеседника
                interlocutor_id = chat.user2_id if chat.user1_id == user_id else chat.user1_id
                interlocutor = await session.get(User, interlocutor_id)

                stmt = text(
                    """
                    SELECT * FROM message
                    WHERE chat_id = :chat_id
                    ORDER BY timestamp DESC
                    LIMIT 1
                    """
                ).bindparams(chat_id=chat.id)
                result = await session.execute(stmt)
                last_message = result.first()

                chat_data = SChatForList(
                    chat_id=chat.id,
                    other_user_id=interlocutor.id,
                    other_user_name=interlocutor.name,
                    other_user_image=interlocutor.image_path,
                    last_message=SMessage(
                        id=last_message.id if last_message else None,
                        content=last_message.content if last_message else None,
                        chat_id=last_message.chat_id if last_message else None,
                        timestamp=last_message.timestamp if last_message else None,
                        sender_id=last_message.sender_id if last_message else None,
                        is_read=last_message.is_read if last_message else None,
                    ) if last_message else None
                )
                
                chat_list.append(chat_data)

        return chat_list


    @classmethod
    async def chat_exists(cls, user1_id: int, user2_id: int):
        async with async_session_maker() as session:
            # Проверим, существует ли уже чат между указанными пользователями
            stmt = (
                select(Chat)
                .filter(
                    ((Chat.user1_id == user1_id) & (Chat.user2_id == user2_id)) |
                    ((Chat.user1_id == user2_id) & (Chat.user2_id == user1_id))
                )
            )
            existing_chat = (await session.execute(stmt)).scalars().first()

            return existing_chat
    

    @classmethod
    async def chat_exists_by_id(cls, chat_id: int) -> Chat:
        async with async_session_maker() as session:
            stmt = (
                select(Chat)
                .where(Chat.id == chat_id)
            )
            existing_chat = (await session.execute(stmt)).scalars().first()

            return existing_chat is not None


    @classmethod
    async def get_massages(cls, chat_id: int, count: int = 20):
        async with async_session_maker() as session:

            stmt = (
                select(Message)
                .options(
                    selectinload(Message.attachments)
                )
                .where(Message.chat_id == chat_id)
                .order_by(Message.timestamp)
                .limit(count)
            )

            result = await session.execute(stmt)
            messages = result.scalars().all()

        return messages


class MessageDAO(BaseDAO[Message, SMessageCreate, SMessageUpdate]):
    model = Message
