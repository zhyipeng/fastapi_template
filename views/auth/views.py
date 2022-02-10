from fastapi import Depends
from fastapi.responses import RedirectResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from core.depends import verify_user
from core.responses import APIResponse
from core.settings import settings
from services.auth import AuthService, OAuthService
from utils import to_dict
from views.auth.schemas import UserSchema

router = InferringRouter()


"""
Zuth登录步骤:
0. 在 Zuth 后台配置 app(redirect_uri设置为 {HOST}/v1/auth/oauth/callback)
1. 前端重定向到 /v1/auth/login
2. Zuth 授权流程
3. Zuth 重定向回 /v1/auth/oauth/callback
4. 带 token 重定向到前端 /login 页
5. 前端保存登录态
"""

@cbv(router)
class AuthView:

    @router.get('/login')
    async def login(self):
        return RedirectResponse(
            url=f'{settings.ZUTH_HOST}/v1/oauth/?appid={settings.ZUTH_APPID}')

    @router.get('/oauth/callback')
    async def oauth_callback(self, code: str):
        async with OAuthService() as svr:
            _, access_token = await svr.handle_callback(code)

        return RedirectResponse(
            f'{settings.CLIENT_HOST}/#/login?token={access_token}')

    @router.get('/userinfo')
    async def get_userinfo(self, uid: int = Depends(verify_user)) -> APIResponse.schema(UserSchema):
        async with AuthService() as svr:
            user = await svr.get_user_by_id(uid)
            return APIResponse.to_response(to_dict(user, excludes=['password']))
