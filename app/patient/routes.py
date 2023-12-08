from typing import Annotated
from fastapi import APIRouter, Depends

from app.auth.auth import current_active_user, current_admin_user
from app.crud_sqlalchemy.sqlalchemy import SQLAlchemyCRUDRouter
from app.database import get_async_session
from app.doctor.schemas import SDoctor
from app.patient.dao import PatientDAO
from app.patient.model import Patient
from app.patient.schemas import SPatientRead, SPatientCreate
from app.user.model import User


router = SQLAlchemyCRUDRouter(
    prefix="/patients",
    tags=["Patient"],
    db_model=Patient,
    schema=SPatientRead,
    delete_all_route=[Depends(current_admin_user)],
    delete_one_route=[Depends(current_admin_user)],
    dependencies=[Depends(current_active_user)]
)
