from enum import Enum
from typing import Any, Generic, TypeVar

from fastapi import HTTPException
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import Select, delete, exc, func, insert, select

from app.logger import logger
from app.database import BaseAlchemyModel, async_session_maker

ModelType = TypeVar("ModelType", bound=BaseAlchemyModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=BaseAlchemyModel)


class IOrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"


class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model: ModelType

    @classmethod
    async def get_one_or_none(cls, *, id: int) -> ModelType | None:
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == id)
            response = await session.execute(query)
            return response.scalar_one_or_none()

    @classmethod
    async def get_by_ids(cls, *, list_ids: list[int]) -> list[ModelType] | None:
        async with async_session_maker() as session:
            response = await session.execute(
                select(cls.model).where(cls.model.id.in_(list_ids))
            )
            return response.scalars().all()

    @classmethod
    async def get_count(cls) -> ModelType | None:
        async with async_session_maker() as session:
            response = await session.execute(
                select(func.count()).select_from(select(cls.model).subquery())
            )
            return response.scalar_one()

    @classmethod
    async def get_multi(
        cls,
        *,
        skip: int = 0,
        limit: int = 100,
        query: T | Select[T] | None = None
    ) -> list[ModelType]:
        async with async_session_maker() as session:
            if query is None:
                query = select(cls.model).offset(skip).limit(limit).order_by(cls.model.id)
            response = await session.execute(query)
            return response.scalars().all()

    @classmethod
    async def get_multi_paginated(
        cls,
        *,
        params: Params | None = Params(),
        query: T | Select[T] | None = None,
    ) -> Page[ModelType]:
        async with async_session_maker() as session:
            if query is None:
                query = select(cls.model)
            return await paginate(session, query, params)

    @classmethod
    async def get_multi_paginated_ordered(
        cls,
        *,
        params: Params | None = Params(),
        order_by: str | None = None,
        order: IOrderEnum | None = IOrderEnum.ascendent,
        query: T | Select[T] | None = None,
    ) -> Page[ModelType]:
        async with async_session_maker() as session:
            columns = cls.model.__table__.columns
            if order_by is None or order_by not in columns:
                order_by = "id"
            if query is None:
                if order == IOrderEnum.ascendent:
                    query = select(cls.model).order_by(columns[order_by].asc())
                else:
                    query = select(cls.model).order_by(columns[order_by].desc())

            return await paginate(session, query, params)

    @classmethod
    async def get_multi_ordered(
        cls,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str | None = None,
        order: IOrderEnum | None = IOrderEnum.ascendent,
    ) -> list[ModelType]:
        async with async_session_maker() as session:
            columns = cls.model.__table__.columns
            if order_by is None or order_by not in columns:
                order_by = "id"
            if order == IOrderEnum.ascendent:
                query = (
                    select(cls.model)
                    .offset(skip)
                    .limit(limit)
                    .order_by(columns[order_by].asc())
                )
            else:
                query = (
                    select(cls.model)
                    .offset(skip)
                    .limit(limit)
                    .order_by(columns[order_by].desc())
                )

            response = await session.execute(query)
            return response.scalars().all()

    @classmethod
    async def create(
        cls,
        *,
        obj_in: CreateSchemaType | ModelType,
        created_by_id: int | str | None = None,
    ) -> ModelType:
        db_obj = cls.model.from_orm(obj_in)  # type: ignore
        async with async_session_maker() as session:
            if created_by_id:
                db_obj.created_by_id = created_by_id
            try:
                session.add(db_obj)
                await session.commit()
            except exc.IntegrityError:
                session.rollback()
                raise HTTPException(
                    status_code=409,
                    detail="Resource already exists",
                )
            await session.refresh(db_obj)
            return db_obj

    @classmethod
    async def update(
        cls,
        *,
        obj_current: ModelType,
        obj_new: UpdateSchemaType | dict[str, Any] | ModelType,
    ) -> ModelType:
        async with async_session_maker() as session:
            if isinstance(obj_new, dict):
                update_data = obj_new
            else:
                update_data = obj_new.model_dump(exclude_unset=True)  # This tells Pydantic to not include the values that were not sent
            for field in update_data:
                setattr(obj_current, field, update_data[field])

            session.add(obj_current)
            await session.commit()
            await session.refresh(obj_current)
            return obj_current

    @classmethod
    async def delete(cls, *, id: int) -> ModelType:
        async with async_session_maker() as session:
            response = await session.execute(
                select(cls.model).where(cls.model.id == id)
            )
            obj = response.scalar_one()
            await session.delete(obj)
            await session.commit()
            return obj

    @classmethod
    async def delete_all(cls) -> None:
        async with async_session_maker() as session:
            await session.execute(delete(cls.model))
            await session.commit()

    @classmethod
    async def add(cls, **data):
        try:
            query = insert(cls.model).values(**data)#.returning(cls.model.id)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (Exception) as e:
            msg = "Unknown Exc: Cannot insert data into table"
            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None
        


    # @classmethod
    # async def add_bulk(cls, *data):
    #     # Для загрузки массива данных [{"id": 1}, {"id": 2}]
    #     # мы должны обрабатывать его через позиционные аргументы *args.
    #     try:
    #         query = insert(cls.model).values(*data).returning(cls.model.id)
    #         async with async_session_maker() as session:
    #             result = await session.execute(query)
    #             await session.commit()
    #             return result.mappings().first()
    #     except (SQLAlchemyError, Exception) as e:
    #         if isinstance(e, SQLAlchemyError):
    #             msg = "Database Exc"
    #         elif isinstance(e, Exception):
    #             msg = "Unknown Exc"
    #         msg += ": Cannot bulk insert data into table"

    #         logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
    #         return None
