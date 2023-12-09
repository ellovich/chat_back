from datetime import datetime
import json
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

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.active_connections.append({"websocket": websocket, "client_id": client_id})

    def disconnect(self, websocket: WebSocket):
        self.active_connections = [conn for conn in self.active_connections if conn["websocket"] != websocket]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, chat_id: int, message_data: dict, add_to_db: bool = True):
        for connection in self.active_connections:
            if connection["client_id"] == chat_id:
                await connection["websocket"].send_text(json.dumps(message_data))
        if add_to_db:
            await self.add_message_to_database(message_data["chat_id"], message_data["sender_id"], message_data["content"])

    @staticmethod
    async def add_message_to_database(chat_id: int, sender_id: int, content: str):
        async with async_session_maker() as session:
            new_message = Message(
                chat_id=chat_id,
                sender_id=sender_id, 
                content=content, 
                timestamp=datetime.now(),
                is_read=False,
                attachments=[]
            )
            session.add(new_message)
            await session.commit()


ws_manager = ConnectionManager()
