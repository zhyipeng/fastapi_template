import asyncio

from fastapi import FastAPI

from core.exceptions import register_exception_handlers
from views import router

app = FastAPI()
app.include_router(router)

register_exception_handlers(app)


if __name__ == '__main__':
    from core.db import initdb
    asyncio.run(initdb())
