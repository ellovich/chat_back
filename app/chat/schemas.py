from typing import Literal
from pydantic import BaseModel, ConfigDict
from datetime import datetime

# CHAT

class SChatBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore
    user1_id: int
    user2_id: int

class SChatCreate(SChatBase):
    pass

class SChatUpdate(BaseModel):
    pass

class SChat(SChatBase):
    model_config = ConfigDict(from_attributes=True)  # type: ignore
    id: int


# ATTACHMENT

class SAttachmentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore
    file_path: str

class SAttachmentCreate(SAttachmentBase):
    pass

class SAttachment(SAttachmentBase):
    model_config = ConfigDict(from_attributes=True)  # type: ignore
    id: int
    message_id: int
    type: Literal["image", "doc"]


# MESSAGE

class SMessageBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore
    content: str
    timestamp: datetime
    is_read: bool


class SMessageCreate(SMessageBase):
    model_config = ConfigDict(from_attributes=True)  # type: ignore
    chat_id: int
    sender_id: int

class SMessageUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore
    is_read: bool

class SMessage(SMessageBase):
    model_config = ConfigDict(from_attributes=True)  # type: ignore
    id: int
    chat_id: int
    sender_id: int
    attachments: list[SAttachment] = []


# CHAT LIST

class SChatForList(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore
    
    chat_id: int
    other_user_id: int
    other_user_name: str | None
    other_user_image: str | None
    last_message: SMessage | None
