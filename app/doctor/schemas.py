from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Json


class SDoctor(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore

    id: int
    user_id: int

    gender: str | None
    birth: date | None

    medical_institution: str | None
    jobTitle: str | None


class SDoctorUpdate(SDoctor):
    pass

class SDoctorCreate(SDoctor):
    pass