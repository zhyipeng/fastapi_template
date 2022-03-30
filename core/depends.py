from asyncio import create_task

from fastapi import Header

from consts.common import RedisKeys
from core.exceptions import AuthenticationError
from core.paginations import Pagination
from core.settings import settings
from utils.redis_helper import redis_cli


async def verify_user(x_token: str = Header(...)) -> int:
    if not x_token:
        raise AuthenticationError

    key = f'{RedisKeys.AUTH_TOKEN_PREFIX}{x_token}'
    uid = await redis_cli.get(key)
    if not uid:
        raise AuthenticationError(error_message='Token 已过期')

    create_task(refresh_token(x_token))
    return int(uid)


async def refresh_token(token: str):
    key = f'{RedisKeys.AUTH_TOKEN_PREFIX}{token}'
    await redis_cli.expire(key, settings.TOKEN_EXPIRE)


async def paginate(page: int = 1, size: int = 20) -> Pagination:
    return Pagination(page=page, size=size)
