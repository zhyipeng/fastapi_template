from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

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
