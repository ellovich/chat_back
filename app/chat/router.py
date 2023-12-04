from typing import List

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy import and_, desc, func, insert, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.chat.dao import ChatDAO, MessageDAO
from app.logger import logger

from app.chat.model import Chat, Message
from app.chat.schemas import SChatCreate, SChatForList, SMessageUpdate, SChatUpdate, SChat, SMessage
from app.database import async_session_maker, get_async_session
from app.doctor.dao import DoctorDAO
from app.patient.dao import PatientDAO
from app.auth.auth import current_active_user
from app.user.model import User


router = APIRouter(
    prefix="/chat", 
    tags=["Chat"]
)


# чаты текущего пользователя
@router.get("/user_chats")
async def get_user_chats(
    user: User = Depends(current_active_user)
    ) -> list[SChatForList]:

    try:
        doctor = await DoctorDAO.find_one_or_none(user_id = user.id)
        patient = await PatientDAO.find_one_or_none(user_id = user.id)
        
        if doctor:
            ChatDAO.get_chats_by_user(user_id = doctor.id)
        elif patient:
            ChatDAO.get_chats_by_user(user_id = patient.id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# создание чата
@router.post("")
async def create_chat(chat: SChatCreate):
    doctor = await DoctorDAO.get_one_or_none(id = chat.doctor_id)
    patient = await PatientDAO.get_one_or_none(id = chat.patient_id)

    if not doctor or not patient:
        return HTTPException(404, detail="Doctor or Patient not found")

    exist_chat = await ChatDAO.find_one_or_none(doctor_id = doctor.id, patient_id = patient.id)
    if exist_chat:
        return HTTPException(409, detail="Chat already exists")

    new_chat = await ChatDAO.create(obj_in=chat)
    return new_chat.id

# создание сообщения
@router.post("/create_message")
async def create_message(message: SMessage):
    chat = await ChatDAO.get_one_or_none(id = message.chat_id)
    if not chat:
        return HTTPException(404, detail="Chat not found")
    
    new_message = await MessageDAO.create(obj_in=message)
    return new_message.id

# прочитывание всех сообщений чата
@router.post("/{chat_id}/read")
async def read_chat(chat_id: int):
    messages = await MessageDAO.get_multi(chat_id = chat_id)
    for m in messages:
        new_message = m
        new_message.is_read = True
        await MessageDAO.update(
            obj_current=m,
            obj_in=new_message
        )

# прочитывание сообщения
@router.put("/read_message")
async def read_message(message_id: int):
    message = await MessageDAO.get_one_or_none(id = message_id)
    if not message:
        return HTTPException(404, detail="Message not found")
    
    new_message = message
    new_message.is_read = True
    await MessageDAO.update(
        obj_current=message,
        obj_in=new_message
    )

# удаление чата
@router.delete("/{chat_id}")
async def delete_chat(chat_id: int):
    exist_chat = await ChatDAO.get_one_or_none(id = chat_id)
    if not exist_chat:
        return HTTPException(404, detail="Chat not found")
    await ChatDAO.delete(chat_id)



class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, sender_id: int, recipient_id: int):
        if message:
            await self.add_message_to_database(message, sender_id, recipient_id)

        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_message_to_database(message: str, sender_id: int, recipient_id: int):
        async with async_session_maker() as session:
            chat = await session.execute(select(Chat).filter_by(doctor_id=sender_id, patient_id=recipient_id)).scalar()
            if chat is None:
                chat = Chat(doctor_id=sender_id, patient_id=recipient_id)
                session.add(chat)
                await session.flush()

            new_message = Message(content=message, sender_id=sender_id, chat=chat)
            session.add(new_message)
            await session.commit()

manager = ConnectionManager()

@router.get("/{chat_id}/last_messages")
async def get_last_messages(
    chat_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> List[SMessage]:
    query = select(Message).where(Message.chat_id==chat_id).order_by(Message.id.desc()).limit(25)
    messages = await session.execute(query)
    return messages.scalars().all()

@router.websocket("/ws/{client_id}/{recipient_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, recipient_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(
                f"User #{client_id} says: {data}",
                sender_id=client_id,
                recipient_id=recipient_id
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(
            f"User #{client_id} left the chat",
            sender_id=client_id,
            recipient_id=recipient_id
        )
