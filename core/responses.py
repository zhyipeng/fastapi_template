from __future__ import annotations

from typing import Any, Optional, Type, TypedDict

from pydantic import BaseModel, create_model
from zhtools.random import uuid4_hex

from core.paginations import Pagination


class ResponseModel(BaseModel):
    data: Any
    page: Pagination = None
    error_code: int = 0
    error_message: str = ''


class EmptyResponse(ResponseModel):
    data: dict = {}


class APIResponse:
    _schemas: dict[str, Type[BaseModel]] = {}
    Empty = EmptyResponse

    @classmethod
    def to_response(cls,
                    data: Any,
                    pagination: Pagination = None) -> ResponseModel:
        return ResponseModel(data=data, page=pagination)

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
                         page=(Optional[Pagination], ...),
                         error_code=0,
                         error_message='')
        cls._schemas[name] = s
        return s
