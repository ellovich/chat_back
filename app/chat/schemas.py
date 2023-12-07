from pydantic import BaseModel, ConfigDict
from datetime import datetime

# CHAT

class SChatBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore
    doctor_user_id: int
    patient_user_id: int

class SChatCreate(SChatBase):
    pass

class SChatUpdate(BaseModel):
    pass

class SChat(SChatBase):
    model_config = ConfigDict(from_attributes=True)  # type: ignore
    id: int


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
    attachments: list[str] = []

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


# CHAT LIST

class SChatForList(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore
    
    chat_id: int
    doctor_id: int 
    patient_id: int
    last_message: SMessage