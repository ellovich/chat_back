from datetime import datetime
from typing import List
from fastapi import WebSocket, WebSocketDisconnect
from app.logger import logger
from app.chat.model import Message
from app.database import async_session_maker
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, chat_id: int, sender_id: int, content: str, add_to_db: bool):
        if add_to_db:
            await self.add_message_to_database(chat_id=chat_id, 
                                               sender_id=sender_id, 
                                               content=content)
        for connection in self.active_connections:
            await connection.send_text(content)

    @staticmethod
    async def add_message_to_database(chat_id: int, sender_id: int, content: str):
        async with async_session_maker() as session:
            new_message = Message(
                chat_id=chat_id,
                sender_id=sender_id, 
                content=content, 
                timestamp = datetime.now(),
                is_read=False,
                attachments = []
            )
            session.add(new_message)
            await session.commit()


ws_manager = ConnectionManager()
