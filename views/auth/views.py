from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from core.depends import verify_user
from core.responses import APIResponse
from services.auth import AuthService
from utils import to_dict
from views.auth.schemas import RegisterSchema, UserSchema

router = InferringRouter()


@cbv(router)
class AuthView:

    @router.post('/register')
    async def register(self, data: RegisterSchema
                       ) -> APIResponse.schema(UserSchema):
        async with AuthService() as svr:
            user = await svr.register(data.username, data.password)
            return APIResponse.to_response(to_dict(user, excludes=['password']))

    @router.post('/login')
    async def login(self, data: RegisterSchema) -> APIResponse.schema(token=str):
        async with AuthService() as svr:
            token = await svr.login(data.username, data.password)
            return APIResponse.to_response({
                'token': token
            })

    @router.post('/userinfo')
    async def get_userinfo(self,
                           uid: int = Depends(verify_user)
                           ) -> APIResponse.schema(UserSchema):
        async with AuthService() as svr:
            user = await svr.get_user_by_id(uid)
            return APIResponse.to_response(
                to_dict(user, includes=['username', 'id']))

    @router.get('/users')
    async def get_users(self) -> APIResponse.schema(UserSchema, to_list=True):
        async with AuthService() as svr:
            users = await svr.get_users()
            return APIResponse.to_response(
                [UserSchema(**to_dict(u, includes=['username', 'id']))
                 for u in users]
            )
