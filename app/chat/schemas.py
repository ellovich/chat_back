from pydantic import BaseModel, ConfigDict

class SChat(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore

    id: int
    doctor_id: int 
    patient_id: int


class SChatCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore

    doctor_id: int 
    patient_id: int



class SChatUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore


class SMessage(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore

    id: int
    chat_id: int
    content: str
    sender_id: int
    is_read: bool = False



class SMessageCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore

    chat_id: int
    content: str
    sender_id: int
    is_read: bool = False


class SMessageUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore

    id: int
    is_read: bool



class SChatForList(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore
    
    chat_id: int
    doctor_id: int 
    patient_id: int
    last_message: SMessage
