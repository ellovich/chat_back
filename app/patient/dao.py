from datetime import date
import json
from fastapi import HTTPException

from sqlalchemy import and_, func, insert, or_, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, selectinload

from app.base.dao import BaseDAO
from app.database import async_session_maker, engine
# from app.doctor.model import Doctor, doctor_patient_association
from app.doctor.schemas import SDoctor
from app.logger import logger
from app.patient.model import Patient
from app.patient.schemas import SPatientCreate, SPatientUpdate

NOT_FOUND = HTTPException(404, "Item not found")


class PatientDAO(BaseDAO[Patient, SPatientCreate, SPatientUpdate]):
    model = Patient

    # @classmethod
    # async def get_all_doctors(cls, patient_id: int) -> list[SDoctor]:
    #     query = (
    #         select(Doctor)
    #         .join(doctor_patient_association)
    #         .join(Patient)
    #         .where(Patient.id == patient_id)
    #     )
    #     async with async_session_maker() as session:
    #         doctors = await session.execute(query)
    #         return doctors.scalars().all()
