from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.model import Chat, Message
from app.chat.schemas import MessageSchema
from app.database import async_session_maker, get_async_session

router = APIRouter(
    prefix="/chat", 
    tags=["Chat"]
)


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


@router.get("{chat_id}/last_messages")
async def get_last_messages(
    chat_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> List[MessageSchema]:
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
