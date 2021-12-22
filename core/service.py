from sqlalchemy.ext.asyncio import AsyncSession

from core.db import Session


class Service:

    def __init__(self):
        self.session: 'AsyncSession' = Session()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self.session.close()
