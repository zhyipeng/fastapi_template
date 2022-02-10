from pathlib import Path

from pydantic import BaseSettings, RedisDsn, AnyUrl


ROOT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    DEBUG: bool = False
    REDIS_DSN: RedisDsn = 'redis://localhost:6379/0'
    MYSQL_DSN: AnyUrl = 'mysql+asyncmy://root:root@localhost/fastapi_app'

    TOKEN_EXPIRE: int = 3600 * 8
    CLIENT_HOST: AnyUrl = 'http://localhost:3002'

    ZUTH_HOST: AnyUrl = 'http://localhost:8000'
    ZUTH_APPID: str = '487b7500dd534dcfab16f705f05163d7'
    ZUTH_APPSECRET: str = '49965bbab567462fb742536267cedca6'


settings = Settings(_env_file=ROOT_DIR / Path('.env'),
                    _env_file_encoding='utf-8')
