from typing import Any, Coroutine, Generator, List, Optional, Type, Union

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta as Model

import app.crud_sqlalchemy._utils
from app.crud_sqlalchemy._base import NOT_FOUND, CRUDGenerator
from app.crud_sqlalchemy._types import DEPENDENCIES, PAGINATION
from app.crud_sqlalchemy._types import PYDANTIC_SCHEMA as SCHEMA
from app.database import async_session_maker

CALLABLE = Coroutine[Any, Any, Model | None]
CALLABLE_LIST = Coroutine[Any, Any, List[Model]]


class SQLAlchemyCRUDRouter(CRUDGenerator[SCHEMA]):
    def __init__(
        self,
        schema: Type[SCHEMA],
        db_model: Model,
        create_schema: Optional[Type[SCHEMA]] = None,
        update_schema: Optional[Type[SCHEMA]] = None,
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None,
        paginate: Optional[int] = None,
        get_all_route: Union[bool, DEPENDENCIES] = True,
        get_one_route: Union[bool, DEPENDENCIES] = True,
        create_route: Union[bool, DEPENDENCIES] = True,
        update_route: Union[bool, DEPENDENCIES] = True,
        delete_one_route: Union[bool, DEPENDENCIES] = True,
        delete_all_route: Union[bool, DEPENDENCIES] = True,
        **kwargs: Any
    ) -> None:

        self.db_model = db_model
        self._pk: str = db_model.__table__.primary_key.columns.keys()[0]
        self._pk_type: type = int

        super().__init__(
            schema=schema,
            create_schema=create_schema,
            update_schema=update_schema,
            prefix=prefix or db_model.__tablename__,
            tags=tags,
            paginate=paginate,
            get_all_route=get_all_route,
            get_one_route=get_one_route,
            create_route=create_route,
            update_route=update_route,
            delete_one_route=delete_one_route,
            delete_all_route=delete_all_route,
            **kwargs
        )


    def _get_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        async def route(
            pagination: PAGINATION = self.pagination,
        ) -> List[Model]:
            async with async_session_maker() as session:
                skip, limit = pagination.get("skip"), pagination.get("limit")

                results = await session.execute(
                    select(self.db_model)
                    .order_by(getattr(self.db_model, self._pk))
                    .limit(limit)
                    .offset(skip)
                )

                db_models = results.unique().scalars().all()

            return db_models

        return route


    def _get_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            item_id: self._pk_type, 
        ) -> Model:
            async with async_session_maker() as session:
                
                result = await session.get(self.db_model, item_id)

                if result:
                    return result
                else:
                    raise NOT_FOUND from None

        return route


    def _create(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            model: self.create_schema,  # type: ignore
        ) -> Model:
            async with async_session_maker() as session:
                try:
                    db_model: Model = self.db_model(**model.dict())
                    session.add(db_model)
                    await session.commit()
                    await session.refresh(db_model)
                    return db_model
                except IntegrityError:
                    await session.rollback()
                    raise HTTPException(422, "Key already exists") from None

        return route


    def _update(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            item_id: self._pk_type,  # type: ignore
            model: self.update_schema,  # type: ignore
        ) -> Model:
            async with async_session_maker() as session:
                try:
                    db_model: Model = await session.get(self.db_model, item_id)
                    if not db_model:
                        raise NOT_FOUND from None

                    for key, value in model.dict(exclude={self._pk}).items():
                        if hasattr(db_model, key):
                            setattr(db_model, key, value)

                    await session.commit()
                    await session.refresh(db_model)

                    return db_model
                except IntegrityError as e:
                    await session.rollback()
                    self._raise(e)

        return route


    def _delete_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        async def route(
        ) -> List[Model]:
            async with async_session_maker() as session:
                session.query(self.db_model).delete()
                await session.commit()
                return await self._get_all()(pagination={"skip": 0, "limit":  None})

        return route


    def _delete_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            item_id: self._pk_type, 
        ) -> Model:
            async with async_session_maker() as session:
                db_model: Model = await session.get(self.db_model, item_id)
                if not db_model:
                    raise NOT_FOUND from None
                session.delete(db_model)
                await session.commit()
                return db_model

        return route
