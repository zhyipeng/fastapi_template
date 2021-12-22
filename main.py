import asyncio

from fastapi import FastAPI

from views import router

app = FastAPI()
app.include_router(router)


if __name__ == '__main__':
    from core.db import initdb
    asyncio.run(initdb())
