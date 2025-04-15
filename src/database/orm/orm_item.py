import logging
from typing import Literal, Sequence, TypeVar, Generic, overload
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, asc, delete, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm.base_schemes import ListDTO, ResponseStatus
from database.postgres_core import Base


_log = logging.getLogger(__name__)


M = TypeVar('M')
I = TypeVar('I', bound=BaseModel)
E = TypeVar('E', bound=BaseModel)
O = TypeVar('O', bound=BaseModel)


class ItemOrm(Generic[M, I, E, O]):
    def __init__(self, model: type[M], input_scheme: type[I], edit_schema: type[E], out_scheme: type[O]) -> None:
        self.model = model
        self.input_scheme = input_scheme
        self.edit_schema = edit_schema
        self.out_scheme = out_scheme

    @overload
    async def add(
        self,
        session: AsyncSession,
        data: I,
        *,
        is_model: Literal[True] = True
    ) -> M: ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        data: I,
        *,
        is_model: Literal[True] = True,
        return_query: Select
    ) -> M: ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        data: I,
        *,
        is_model: Literal[False]
    ) -> O: ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        data: I,
        *,
        is_model: Literal[False],
        return_query: Select
    ) -> O: ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        data: I,
        is_return: Literal[False]
    ) -> None: ...

    async def add(
        self,
        session: AsyncSession,
        data: I,
        is_return: bool = True,
        is_model: bool = True,
        return_query: Select | None = None
    ) -> M | O | None:
        _log.info("Add %s", self.model.__name__)

        model = self.model(**data.model_dump())
        session.add(model)
        await session.flush()

        if return_query is not None:
            return_query = return_query.filter(
                self.model.id == model.id  # type: ignore
            )
            r = await session.execute(return_query)
            model = r.scalars().first()

        if not is_return:
            return None

        if is_model:
            return model

        return self.out_scheme.model_validate(model)

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        query_select: Select | None = None,
        search: str | None = None,
        search_fields: list[str] | None = None,
        sort_by: str | None = None,
        desc_int: int = 0,
        page: int = 1,
        limit: int = -1,
        has_is_active: bool = False,
        *,
        is_pagination: Literal[True] = True,
        is_model: Literal[False] = False
    ) -> ListDTO[O]: ...

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        query_select: Select | None = None,
        search: str | None = None,
        search_fields: list[str] | None = None,
        sort_by: str | None = None,
        desc_int: int = 0,
        page: int = 1,
        limit: int = -1,
        *,
        has_is_active: bool = False,
        is_pagination: Literal[True],
        is_model: Literal[True]
    ) -> ListDTO[M]: ...

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        query_select: Select | None = None,
        search: str | None = None,
        search_fields: list[str] | None = None,
        sort_by: str | None = None,
        desc_int: int = 0,
        page: int = 1,
        limit: int = -1,
        has_is_active: bool = False,
        *,
        is_pagination: Literal[False],
        is_model: Literal[True]
    ) -> Sequence[M]: ...

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        query_select: Select | None = None,
        search: str | None = None,
        search_fields: list[str] | None = None,
        sort_by: str | None = None,
        desc_int: int = 0,
        page: int = 1,
        limit: int = -1,
        has_is_active: bool = False,
        *,
        is_pagination: Literal[False],
        is_model: Literal[False]
    ) -> Sequence[O]: ...

    async def get_all(
        self,
        session: AsyncSession,
        query_select: Select | None = None,
        search: str | None = None,
        search_fields: list[str] | None = None,
        sort_by: str | None = None,
        desc_int: int = 0,
        page: int = 1,
        limit: int = -1,
        has_is_active: bool = False,
        is_pagination: bool = True,
        is_model: bool = True
    ) -> ListDTO[O] | Sequence[O] | ListDTO[M] | Sequence[M]:
        _log.info("Get all %s", self.model.__name__)

        if query_select is None:
            query_select = select(
                self.model
            )

        if search and search_fields:
            search_conditions = []
            for field in search_fields:
                if hasattr(self.model, field):
                    column = getattr(self.model, field)
                    search_conditions.append(
                        column.ilike(f"%{search}%"))  # type: ignore

            if search_conditions:
                query_select = query_select.filter(or_(*search_conditions))

        if page < 1:
            raise HTTPException(
                status_code=400, detail="Page number must be greater than 0"
            )

        if has_is_active:
            query_select = query_select.filter(
                self.model.is_active == True)  # type: ignore

        if is_pagination:
            q_total_record = query_select

        if sort_by:
            query_select = query_select.order_by(
                desc(getattr(self.model, sort_by)) if desc_int else asc(
                    getattr(self.model, sort_by))
            )

        query_select = query_select.offset((page - 1) * limit)
        if limit != -1:
            query_select = query_select.limit(limit)

        result = await session.execute(query_select)
        content = result.scalars().all()

        if is_pagination:
            q_total_record = q_total_record.with_only_columns(
                func.count(self.model.id))  # type: ignore
            r_total_record = await session.execute(q_total_record)
            total_record = r_total_record.scalar_one_or_none()

            if total_record is None:
                total_record = 0

            if limit == -1:
                pages = 1
            else:
                pages = total_record // limit if total_record % limit == 0 else total_record // limit + 1

            if is_model:
                return ListDTO[M](
                    page_number=page,
                    page_size=limit if limit != -1 else total_record,
                    total_pages=pages,
                    total_record=total_record,
                    content=[item for item in content]
                )
            else:
                return ListDTO[O](
                    page_number=page,
                    page_size=limit if limit != -1 else total_record,
                    total_pages=pages,
                    total_record=total_record,
                    content=[self.out_scheme.model_validate(
                        item) for item in content]
                )
        else:
            if is_model:
                return content
            else:
                return [self.out_scheme.model_validate(item) for item in content]

    @overload
    async def get_by(
        self,
        session: AsyncSession,
        id: UUID | None = None,
        *,
        is_model: Literal[False] = False,
        is_get_none: Literal[False] = False,
        **kwargs
    ) -> O: ...

    @overload
    async def get_by(
        self,
        session: AsyncSession,
        id: UUID | None = None,
        *,
        is_model: Literal[True] = True,
        is_get_none: Literal[False] = False,
        **kwargs
    ) -> M: ...

    @overload
    async def get_by(
        self,
        session: AsyncSession,
        id: UUID | None = None,
        *,
        is_model: Literal[True],
        is_get_none: Literal[True],
        **kwargs
    ) -> M | None: ...

    @overload
    async def get_by(
        self,
        session: AsyncSession,
        id: UUID | None = None,
        *,
        is_model: Literal[False],
        is_get_none: Literal[True],
        **kwargs
    ) -> O | None: ...

    async def get_by(
            self,
            session: AsyncSession,
            id: UUID | None = None,
            is_model: bool = False,
            is_get_none: bool = False,
            **kwargs) -> O | M | None:
        _log.info("Get by kwargs %s", self.model.__name__)

        query = select(
            self.model
        )

        if id is not None:
            query = query.filter_by(id=id)

        query = query.filter_by(
            **kwargs
        )

        result = await session.execute(query)
        item = result.scalars().first()

        if item is None:
            if is_get_none:
                return None
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        if is_model:
            return item

        return self.out_scheme.model_validate(item)

    @overload
    async def get_by_query(
        self,
        session: AsyncSession,
        query: Select,
        id: UUID | None = None,
        is_model: Literal[True] = True,
        is_get_none: Literal[False] = False,
    ) -> M: ...

    @overload
    async def get_by_query(
        self,
        session: AsyncSession,
        query: Select,
        id: UUID | None = None,
        is_model: Literal[False] = False,
        is_get_none: Literal[False] = False,
    ) -> O: ...

    @overload
    async def get_by_query(
        self,
        session: AsyncSession,
        query: Select,
        id: UUID | None = None,
        is_model: Literal[True] = True,
        is_get_none: Literal[True] = True,
    ) -> M | None: ...

    @overload
    async def get_by_query(
        self,
        session: AsyncSession,
        query: Select,
        id: UUID | None = None,
        is_model: Literal[False] = False,
        is_get_none: Literal[True] = True,
    ) -> O | None: ...

    async def get_by_query(
        self,
        session: AsyncSession,
        query: Select,
        id: UUID | None = None,
        is_model: bool = True,
        is_get_none: bool = True,
    ) -> O | M | None:
        _log.info("Get by query %s", self.model.__name__)

        if id is not None:
            query = query.filter_by(id=id)

        result = await session.execute(query)
        model = result.scalars().first()

        if model is None:
            if is_get_none:
                return None
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        if is_model:
            return model

        return self.out_scheme.model_validate(model)

    @overload
    async def edit(
        self,
        session: AsyncSession,
        id: UUID,
        edit_item: E | dict,
        is_model: Literal[True],
    ) -> M: ...

    @overload
    async def edit(
        self,
        session: AsyncSession,
        id: UUID,
        edit_item: E | dict,
        is_model: Literal[False],
    ) -> O: ...

    @overload
    async def edit(
        self,
        session: AsyncSession,
        id: UUID,
        edit_item: E | dict,
        is_model: Literal[True],
        return_query: Select,
    ) -> M: ...

    @overload
    async def edit(
        self,
        session: AsyncSession,
        id: UUID,
        edit_item: E | dict,
        is_model: Literal[False],
        return_query: Select,
    ) -> O: ...

    async def edit(
        self,
        session: AsyncSession,
        id: UUID,
        edit_item: E | dict,
        is_model: bool = True,
        return_query: Select | None = None
    ) -> O | M | None:
        _log.info("Edit %s", self.model.__name__)

        model = await session.get(self.model, id)

        if model is None:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        if isinstance(edit_item, dict):
            for key, value in edit_item.items():
                if value is not None:
                    setattr(model, key, value)
        else:
            for key, value in edit_item.model_dump().items():
                if value is not None:
                    setattr(model, key, value)

        await session.flush()

        if return_query is not None:
            if is_model:
                return await self.get_by_query(
                    session=session,
                    query=return_query,
                    is_model=True,
                    is_get_none=False
                )

            return await self.get_by_query(
                session=session,
                query=return_query,
                is_model=False,
                is_get_none=False
            )

        if is_model:
            return model

        return self.out_scheme.model_validate(model)

    async def in_db(self, session: AsyncSession, item_ids: list[UUID]) -> bool:
        _log.info("In db %s", self.model.__name__)

        for institute_id in item_ids:
            query = select(self.model).filter(
                self.model.id == institute_id)  # type: ignore
            result = await session.execute(query)
            institute = result.scalars().first()
            if institute is None:
                return False
        return True

    @overload
    async def delete(
        self,
        session: AsyncSession,
        id: UUID
    ) -> ResponseStatus: ...

    @overload
    async def delete(
        self,
        session: AsyncSession,
        id: UUID,
        query_has_child: Select
    ) -> ResponseStatus: ...

    async def delete(
        self,
        session: AsyncSession,
        id: UUID,
        query_has_child: Select | None = None
    ) -> ResponseStatus:
        _log.info("Delete %s", self.model.__name__)

        model = None
        if query_has_child is not None:
            res = await session.execute(query_has_child)
            model = res.scalars().first()

        if model is not None:
            await self.edit(
                session=session,
                id=id,
                edit_item={"is_active": False},
                is_model=True
            )
        else:
            del_model = await session.get(self.model, id)

            if del_model is None:
                raise HTTPException(
                    status_code=404, detail=f"{self.model.__name__} not found")

            await session.execute(
                delete(self.model).where(self.model.id == id)
            )
            await session.flush()

        return ResponseStatus()

    async def query(self, session: AsyncSession, query: Select) -> Result:
        _log.info("Query %s", self.model.__name__)

        result = await session.execute(query)
        return result


class BaseItemOrm:
    def __init__(self) -> None:
        pass

    async def get_all_query(self, session: AsyncSession, query: Select) -> Sequence:
        _log.info("Base query")

        result = await session.execute(query)
        items = result.scalars().all()

        return items

    async def get_dict_query(self, session: AsyncSession, query: Select) -> dict:
        _log.info("Base query")

        result = await session.execute(query)
        items = result.tuples().all()

        return {item[0]: item[1] for item in items}

    async def get_tuple_query(self, session: AsyncSession, query: Select) -> Sequence:
        _log.info("Base query")

        result = await session.execute(query)
        items = result.tuples().all()

        return items
