import enum
from typing import Literal, Optional

from fastapi_users import schemas
from pydantic import ConfigDict, EmailStr, constr
from sqlalchemy import Enum, String


class SUserCreate(schemas.BaseUserCreate):
    model_config = ConfigDict(from_attributes=True)  # type: ignore

    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    type: Literal["patient", "doctor"]
    name: Optional[str]
    phone_number: Optional[str]
    image_path: str | None


class SUserRead(schemas.BaseUser[int]):
    model_config = ConfigDict(from_attributes=True)  # type: ignore

    id: int
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    type: str
    name: Optional[str]
    phone_number: str
    image_path: str | None


class SUserUpdate(schemas.BaseUserUpdate):
    model_config = ConfigDict(from_attributes=True)  # type: ignore
