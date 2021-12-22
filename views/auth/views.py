from fastapi import HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status

from services.auth import AuthService
from utils import to_dict
from views.auth.schemas import RegisterSchema, UserSchema

router = InferringRouter()


@cbv(router)
class AuthView:

    @router.post('/register')
    async def register(self, data: RegisterSchema) -> UserSchema:
        async with AuthService() as svr:
            user = await svr.get_user(data.username)
            if user:
                raise HTTPException(status_code=status.HTTP_200_OK,
                                    detail='用户已存在')

            user = await svr.create_user(data.username, data.password)
            return to_dict(user, excludes=['password'])

    @router.post('/login')
    async def login(self, data: RegisterSchema) -> UserSchema:
        async with AuthService() as svr:
            user = await svr.get_user(data.username)
            if user and await svr.check_password(user, data.password):
                return to_dict(user, excludes=['password'])

            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail='账号或密码错误')
