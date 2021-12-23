from fastapi import Header

from consts.common import RedisKeys
from core.exceptions import AuthenticationError
from utils.redis_helper import redis_cli


async def verify_user(x_token: str = Header(...)):
    if not x_token:
        raise AuthenticationError

    key = f'{RedisKeys.AUTH_TOKEN_PREFIX}{x_token}'
    uid = redis_cli.get(key)
    if not uid:
        raise AuthenticationError('Token 已过期')

    return uid
