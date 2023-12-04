from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Json


class SDoctor(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore

    id: int
    first_name: str
    middle_name: str | None
    last_name: str

    # fullName: str
    gender: str  # Literal["М", "Ж"]
    birth: date
    image_path: str | None

    medical_institution: str | None
    jobTitle: str | None
    contacts: dict
    education: dict
    career: dict 


class SDoctorUpdate(SDoctor):
    pass

class SDoctorCreate(SDoctor):
    pass