from __future__ import annotations

from typing import Any, Type, TypedDict

from pydantic import BaseModel, create_model
from zhtools.random import uuid4_hex


class ResponseModel(BaseModel):
    data: Any
    error_code: int = 0
    error_message: str = ''


class APIResponse:
    _schemas: dict[str, Type[BaseModel]] = {}

    @classmethod
    def to_response(cls, data: Any) -> ResponseModel:
        return ResponseModel(data=data)

    @classmethod
    def schema(cls,
               model: Type[BaseModel] | TypedDict = None,
               **kwargs) -> Type[BaseModel]:
        if not model:
            model = TypedDict(uuid4_hex(), kwargs)

        name = 'APIResponse' + model.__name__
        if name in cls._schemas:
            return cls._schemas[name]

        s = create_model(name,
                         data=(model, ...),
                         error_code=0,
                         error_message='')
        cls._schemas[name] = s
        return s
