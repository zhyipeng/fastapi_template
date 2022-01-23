from __future__ import annotations

from typing import Any, Type, TypedDict

from pydantic import BaseModel, create_model
from zhtools.random import uuid4_hex


class ResponseModel(BaseModel):
    data: Any
    error_code: int = 0
    error_message: str = ''


class EmptyResponse(ResponseModel):
    data: dict = {}


class APIResponse:
    _schemas: dict[str, Type[BaseModel]] = {}
    Empty = EmptyResponse

    @classmethod
    def to_response(cls, data: Any) -> ResponseModel:
        return ResponseModel(data=data)

    @classmethod
    def empty_response(cls) -> EmptyResponse:
        return EmptyResponse()

    @classmethod
    def schema(cls,
               model: Type[BaseModel] | TypedDict = None,
               to_list: bool = False,
               **kwargs) -> Type[BaseModel]:
        if not model:
            model = TypedDict(uuid4_hex(), kwargs)

        name = 'APIResponse' + model.__name__
        if to_list:
            name += 'List'
        if name in cls._schemas:
            return cls._schemas[name]

        if to_list:
            data = (list[model], ...)
        else:
            data = (model, ...)

        s = create_model(name,
                         data=data,
                         error_code=0,
                         error_message='')
        cls._schemas[name] = s
        return s
