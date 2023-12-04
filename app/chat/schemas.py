from pydantic import BaseModel, ConfigDict


class MessageSchema(BaseModel):
    id: int
    doctor_id: int 
    patient_id: int
    content: str

    model_config = ConfigDict(from_attributes=True)  # type: ignore
