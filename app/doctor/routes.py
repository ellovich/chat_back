from fastapi import APIRouter, Depends

from app.auth.auth import current_active_user, current_admin_user
from app.crud_sqlalchemy.sqlalchemy import SQLAlchemyCRUDRouter
from app.doctor.dao import DoctorDAO
from app.doctor.model import Doctor
from app.doctor.schemas import SDoctor, SDoctorCreate, SDoctorUpdate
from app.patient.model import Patient
from app.patient.schemas import SPatientRead
from app.user.model import User

router = SQLAlchemyCRUDRouter(
    prefix="/doctor",
    tags=["Doctor"],
    db_model=Doctor,
    schema=SDoctor, 
    delete_all_route=[Depends(current_admin_user)],
    delete_one_route=[Depends(current_admin_user)],
    dependencies=[Depends(current_active_user)]     
)

# @router.get("/{id}/patients")
# async def get_doctor_patients(id: int) -> list[SPatientRead]:
#     return await DoctorDAO.get_doctor_patients(doctor_id=id)