import asyncio
import os

import typer
from fastapi import FastAPI

from core.exceptions import register_exception_handlers
from core.middlewares import use_middlewares
from views import router

app = FastAPI()
app.include_router(router)

use_middlewares(app)
register_exception_handlers(app)

cli = typer.Typer()


@cli.command()
def initdb():
    """更新数据表"""
    # from core.db import initdb
    # asyncio.run(initdb())
    os.system('./venv/bin/alembic upgrade head')


@cli.command()
def genmigration(message: str = None):
    """生成migration脚本"""
    if not message:
        message = input('Input migration message: ')
    os.system(f"./venv/bin/alembic revision --autogenerate -m '{message}'")


@cli.command()
def destorydb():
    """删除数据表"""
    inp = input('⚠️此操作将删除所有数据, 是否继续? (Y/N) ')
    if inp in 'yY':
        from core.db import dropdb
        asyncio.run(dropdb())


if __name__ == '__main__':
    cli()
