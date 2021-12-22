from asyncio import current_task
from typing import AsyncContextManager

from sqlalchemy import Column
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_scoped_session,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker
from zhtools.convertors import camel_case_to_underline


class ModelMeta(DeclarativeMeta):
    def __new__(typ, name, bases, attrs):
        obj = DeclarativeMeta.__new__(typ, name, bases, attrs)
        if name != 'Base':
            obj.__tablename__ = camel_case_to_underline(name)
            for k, v in attrs.items():
                if isinstance(v, Column) and v.primary_key:
                    obj.pk = getattr(obj, k)

        return obj


def create_engine() -> AsyncEngine:
    url = 'mysql+asyncmy://root:root@localhost/eyes'
    return create_async_engine(url, echo=True, pool_recycle=1800)


engine = create_engine()


BaseModel = declarative_base(metaclass=ModelMeta)


def create_async_session() -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


_async_sessionmaker = create_async_session()


def Session() -> AsyncContextManager[AsyncSession] | AsyncSession:
    _Session = async_scoped_session(_async_sessionmaker,
                                    scopefunc=current_task)
    return _Session()


async def initdb():
    engine = create_engine()
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
