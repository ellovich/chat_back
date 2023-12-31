from typing import List

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy.orm import joinedload
from sqlalchemy import and_, desc, func, insert, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.dao import ChatDAO, MessageDAO
from app.logger import logger
from app.chat.model import Chat, Message
from app.chat.schemas import SChatCreate, SChatForList, SMessageUpdate, SChatUpdate, SChat, SMessage
from app.database import async_session_maker, get_async_session
from app.doctor.dao import DoctorDAO
from app.patient.dao import PatientDAO
from app.auth.auth import current_active_user, current_admin_user
from app.user.model import User


router = APIRouter(
    prefix="/chats", 
    tags=["Chat"]
)

@router.get("")
async def get_my_chats_list(
    current_user: User = Depends(current_active_user),
) -> list[SChatForList]:
    return await ChatDAO.get_chats_list_by_user_id(current_user.id)


@router.post("")
async def create_chat(
    other_user_id: int,
    current_user: User = Depends(current_active_user),
):
    async with async_session_maker() as session:
        # Убедимся, что указанный пользователь существует
        other_user = await session.get(User, other_user_id)
        if not other_user:
            raise HTTPException(status_code=404, detail="Пользователь с указанным ID не найден.")

        # Убедимся, что текущий пользователь и указанный пользователь различны
        if current_user.id == other_user.id:
            raise HTTPException(status_code=400, detail="Нельзя создать чат с самим собой.")

        existing_chat = await ChatDAO.chat_exists(current_user.id, other_user.id)
        if existing_chat:
            raise HTTPException(status_code=400, detail="Чат уже существует между указанными пользователями.")

        # Создадим новый чат
        new_chat = Chat(user1_id=current_user.id, user2_id=other_user.id)
        session.add(new_chat)
        await session.commit()

        return {
            "chat_id": new_chat.id,
            "user1_id": new_chat.user1_id,
            "user2_id": new_chat.user2_id,
        }


@router.delete("")
async def delete_all(user: User = Depends(current_admin_user)):
    await ChatDAO.delete_all()
    return {"message": "Все чаты удалены"}


@router.get("/{id}")
async def get_my_chat_messages(
    id: int,
    current_user: User = Depends(current_active_user),
    count: int = 2000,
) -> list[SMessage]:
    
    # Проверяем, существует ли чат
    exist_chat = await ChatDAO.get_one_or_none(id=id)
    if not exist_chat:
        raise HTTPException(404, detail="Чат не найден")
    
    # Проверяем, что текущий пользователь участвует в чате
    if current_user.id not in (exist_chat.user1_id, exist_chat.user2_id):
        raise HTTPException(403, detail="Нет прав на удаление этого чата")

    return await ChatDAO.get_massages(id, count)


@router.delete("/{id}")
async def delete_one_my(id: int, current_user: User = Depends(current_active_user)):
    # Проверяем, существует ли чат
    exist_chat = await ChatDAO.get_one_or_none(id=id)
    if not exist_chat:
        raise HTTPException(404, detail="Чат не найден")
    
    # Проверяем, что текущий пользователь участвует в чате
    if current_user.id not in (exist_chat.user1_id, exist_chat.user2_id):
        raise HTTPException(403, detail="Нет прав на удаление этого чата")

    await ChatDAO.delete(id=id)

    return {"message": "Чат удален"}


@router.put("/{id}/read")
async def read_chat(id: int, current_user: User = Depends(current_active_user)):    
    # Проверяем, существует ли чат
    exist_chat = await ChatDAO.get_one_or_none(id=id)
    if not exist_chat:
        raise HTTPException(404, detail="Чат не найден")
    
    # Проверяем, что текущий пользователь участвует в чате
    if current_user.id not in (exist_chat.user1_id, exist_chat.user2_id):
        raise HTTPException(403, detail="Нет прав на удаление этого чата")

    messages = await ChatDAO.get_massages(chat_id = id)
    for m in messages:
        new_message = m
        new_message.is_read = True
        await MessageDAO.update(
            obj_current=m,
            obj_in=new_message
        )
    return {"message": "Сообщение прочитаны"}
