from datetime import date

from sqlalchemy import and_, func, or_, select

from app.base.dao import BaseDAO
from app.database import async_session_maker, engine
from app.doctor.model import Doctor #, doctor_patient_association
from app.doctor.schemas import SDoctor, SDoctorCreate, SDoctorUpdate
from app.logger import logger
from app.patient.model import Patient


class DoctorDAO(BaseDAO[Patient, SDoctorCreate, SDoctorUpdate]):
    model = Doctor

    # @classmethod
    # async def get_doctor_patients(cls, doctor_id: int) -> list[SPatient]:
    #     q_patients = (
    #         select(Patient)
    #         .join(doctor_patient_association)
    #         .join(Doctor)
    #         .where(Doctor.id == doctor_id)
    #     )

    #     async with async_session_maker() as session:
    #         logger.debug(
    #             q_patients.compile(engine, compile_kwargs={"literal_binds": True})
    #         )
    #         patients = await session.execute(q_patients)
    #         return patients.scalars().all()


    # @classmethod
    # async def find_colleagues_by_patient(cls, patient_id: int) -> list[SDoctor]:
    #     q_colleagues = (
    #         select(Doctor)
    #         .join(doctor_patient_association)
    #         .join(Patient)
    #         .where(Patient.id == patient_id)
    #     )

    #     async with async_session_maker() as session:
    #         logger.debug(
    #             q_colleagues.compile(engine, compile_kwargs={"literal_binds": True})
    #         )
    #         colleagues = await session.execute(q_colleagues)
    #         return colleagues.scalars().all()
