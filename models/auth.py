import time

from sqlalchemy import Column, Integer, String

from core.db import BaseModel


class User(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True)
    password = Column(String(256), default='')
    created = Column(Integer, default=time.time, index=True)
