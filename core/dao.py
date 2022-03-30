import typing

from sqlalchemy import func, select, delete
from sqlalchemy.engine import Result

if typing.TYPE_CHECKING:
    from sqlalchemy.orm import Query
    from sqlalchemy.ext.asyncio import AsyncSession
    from core.paginations import Pagination
    from core.db import BaseModel


class Dao:

    def __init__(self, session: 'AsyncSession'):
        self.session = session

    async def _get_one(self, stmt: 'Query') -> typing.Optional['BaseModel']:
        if stmt._limit_clause is None:
            stmt = stmt.limit(1)
        result: 'Result' = await self.session.execute(stmt)
        return result.scalars().first()

    async def _get_count(self,
                         model: typing.Type['BaseModel'],
                         *filters) -> int:
        stmt = select(func.count(model.pk))
        if filters:
            stmt = stmt.filter(*filters)
        result: 'Result' = await self.session.execute(stmt)
        return result.scalars().first()

    async def _get_list(self, stmt: 'Query') -> list['BaseModel']:
        result: 'Result' = await self.session.execute(stmt)
        return result.scalars().all()

    async def _get_rows(self, stmt: 'Query') -> list[tuple]:
        result: 'Result' = await self.session.execute(stmt)
        return result.all()

    async def execute_and_commit(self, stmt: 'Query'):
        await self.session.execute(stmt)
        await self.session.commit()


class CurdMixin:
    Model: typing.ClassVar['BaseModel']

    async def get_one(self,
                      pk: int,
                      options: typing.Sequence[typing.Any] = None
                      ) -> typing.Optional['BaseModel']:
        stmt: 'Query' = select(self.Model)
        if options:
            stmt = stmt.options(*options)

        stmt = stmt.where(self.Model.pk == pk).limit(1)
        return await self._get_one(stmt)

    async def get_all(self,
                      *filters,
                      pagination: 'Pagination' = None,
                      options: typing.Sequence[typing.Any] = None,
                      order_by: typing.Sequence[typing.Any] = None
                      ) -> list['BaseModel']:
        stmt: 'Query' = select(self.Model)
        if options:
            stmt = stmt.options(*options)
        if filters:
            stmt = stmt.filter(*filters)
        if order_by:
            stmt = stmt.order_by(*order_by)

        if pagination:
            total = await self._get_count(self.Model, *filters)
            pagination.total = total
            if not total:
                return []

            stmt = stmt.offset(
                pagination.offset).limit(pagination.limit)

        return await self._get_list(stmt)

    async def get_count(self, *filters) -> int:
        return await self._get_count(self.Model, *filters)

    async def save(self, model: 'BaseModel'):
        self.session.add(model)
        await self.session.commit()

    async def bulk_save(self, models: list['BaseModel']):
        self.session.bulk_save_objects(models)
        await self.session.commit()

    async def delete(self, ids: list[int]):
        stmt = delete(self.Model).filter(self.Model.pk.in_(ids))
        await self.execute_and_commit(stmt)
