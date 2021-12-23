from __future__ import annotations

from typing import Any

from fastapi import Request
from starlette import status
from starlette.responses import JSONResponse


class BusinessException(Exception):

    def __init__(self,
                 error_code: int,
                 error_message: str,
                 error_data: Any = None):
        self.error_code = error_code
        self.error_message = error_message
        self.error_data = error_data

    def __str__(self):
        return f'BusinessException: {self.error_code}-{self.error_message}'

    def __call__(self,
                 error_code: int = None,
                 error_message: str = None,
                 error_data: Any = None,
                 ) -> BusinessException:
        return BusinessException(error_code or self.error_code,
                                 error_message or self.error_message,
                                 error_data or self.error_data)


AuthenticationError = BusinessException(20001, '未登录')


def handle_business_exception(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'error_code': exc.error_code,
            'error_message': exc.error_message,
            'error_data': exc.error_data,
        }
    )
