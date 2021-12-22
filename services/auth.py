import hashlib
import typing

from core.service import Service
from dao import AuthDao
from models.auth import User


class AuthService(Service):

    @property
    def dao(self):
        return AuthDao(self.session)

    @staticmethod
    def encrypt_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    async def get_user(self, username: str) -> typing.Optional[User]:
        return await self.dao.get_user_by_name(username)

    async def check_password(self, user: User, password: str) -> bool:
        return user.password == self.encrypt_password(password)

    async def create_user(self,
                          username: str,
                          password: str) -> typing.Optional[User]:
        password = self.encrypt_password(password)
        return await self.dao.create_user(username, password)
