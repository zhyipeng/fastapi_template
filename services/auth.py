import hashlib
import typing

from zhtools.random import uuid4_hex

from consts.common import RedisKeys
from core.exceptions import AuthenticationError
from core.service import Service
from core.settings import settings
from dao import AuthDao
from models.auth import User
from utils.redis_helper import redis_cli


class AuthService(Service):

    @property
    def dao(self):
        return AuthDao(self.session)

    @staticmethod
    def encrypt_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    async def get_users(self) -> list[User]:
        return await self.dao.get_all()

    async def get_user(self, username: str) -> typing.Optional[User]:
        return await self.dao.get_user_by_name(username)

    async def get_user_by_id(self, uid: int) -> typing.Optional[User]:
        user = await self.dao.get_one(uid)
        if not user:
            raise AuthenticationError(error_message='用户不存在')
        return user

    async def check_password(self, user: User, password: str) -> bool:
        return user.password == self.encrypt_password(password)

    async def create_user(self,
                          username: str,
                          password: str) -> typing.Optional[User]:
        password = self.encrypt_password(password)
        return await self.dao.create_user(username, password)

    async def gen_token(self, user: User):
        token = uuid4_hex()
        key = f'{RedisKeys.AUTH_TOKEN_PREFIX}{token}'
        await redis_cli.set(key, user.id, settings.TOKEN_EXPIRE)
        return token

    async def refresh_token(self, token: str):
        key = f'{RedisKeys.AUTH_TOKEN_PREFIX}{token}'
        await redis_cli.expire(key, settings.TOKEN_EXPIRE)

    async def register(self,
                       username: str,
                       password: str) -> User:
        if await self.get_user(username):
            raise AuthenticationError(error_message='用户已存在')

        return await self.create_user(username, password)

    async def login(self, username: str, password: str) -> str:
        user = await self.get_user(username)
        if user and await self.check_password(user, password):
            return await self.gen_token(user)

        raise AuthenticationError(error_message='用户名或密码错误')
