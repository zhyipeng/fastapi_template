import typing

from sqlalchemy import select

from core.dao import CurdMixin, Dao
from models.auth import User


class AuthDao(CurdMixin, Dao):
    Model = User

    async def get_user_by_name(self, username: str) -> typing.Optional[User]:
        stmt = select(User).filter(User.username == username)
        return await self._get_one(stmt)

    async def create_user(self, username: str, password: str) -> User:
        user = User(username=username, password=password)
        await self.save(user)
        return user

    async def get_or_create_user(self, uid: int, username: str) -> User:
        user = await self.get_one(uid)
        if not user:
            user = User(id=uid, username=username)
            await self.save(user)

        return user
