from pathlib import Path

from pydantic import BaseSettings, RedisDsn, AnyUrl


ROOT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    DEBUG: bool = False
    REDIS_DSN: RedisDsn = 'redis://localhost:6379/0'
    MYSQL_DSN: AnyUrl = 'mysql+asyncmy://root:root@localhost/fastapi_app'

    TOKEN_EXPIRE: int = 3600 * 8


settings = Settings(_env_file=ROOT_DIR / Path('.env'),
                    _env_file_encoding='utf-8')
