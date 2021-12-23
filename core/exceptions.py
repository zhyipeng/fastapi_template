from __future__ import annotations

from typing import Any

from fastapi import Request, FastAPI
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
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


def handle_request_validation_error(request: Request,
                                    exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'error_code': 10001,
            'error_message': '参数格式错误',
            'error_data': exc.errors()
        }
    )


def handle_http_error(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'error_code': 10000,
            'error_message': exc.detail,
            'error_data': exc.detail
        }
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(BusinessException, handle_business_exception)
    app.add_exception_handler(RequestValidationError,
                              handle_request_validation_error)
    app.add_exception_handler(StarletteHTTPException, handle_http_error)
