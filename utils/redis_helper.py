import aioredis

from core.settings import settings


def get_redis_client(decode_responses: bool = False) -> aioredis.Redis:
    return aioredis.from_url(settings.REDIS_DSN,
                             decode_responses=decode_responses)


redis_cli = get_redis_client(True)
