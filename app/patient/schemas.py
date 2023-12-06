from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Json


class SPatientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore

    id: int
    user_id: int
    gender: Literal["М", "Ж"] | None
    birth_date: date | None


class SPatientCreate(BaseModel):
    id: int
    # email: str
    # password: str
    # type: str = "patient"
    model_config = ConfigDict(from_attributes=True)  # type: ignore
    # id: int
    # gender: Literal["М", "Ж"]
    # birth_date: date
    # status: str | None
    # discussion: int | None
    # comment: str | None
    # attribs: Json

class SPatientUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # type: ignore

    # id: int
    gender: Literal["М", "Ж"]
    birth_date: date
    status: str | None
    discussion: int | None
    comment: str | None
    attribs: Json
