from typing import Optional

from zhtools.api_service import (APIPath, AsyncGetAPI, AsyncPostAPI,
                                 RequestMethod, Service)

from core.exceptions import ExternalServerError
from core.settings import settings


class ZuthAPI(APIPath):
    GET_ACCESS_TOKEN = '/v1/oauth/access_token'
    GET_USERINFO = '/v1/oauth/userinfo'


class ZuthService(Service):
    HOST = settings.ZUTH_HOST

    get_access_token = AsyncPostAPI(ZuthAPI.GET_ACCESS_TOKEN,
                                    'code',
                                    appid=settings.ZUTH_APPID)
    get_userinfo = AsyncGetAPI(ZuthAPI.GET_USERINFO, 'access_token')

    def handle_result(self, result: dict):
        if result.get('error_code') != 0:
            raise ExternalServerError(error_data=result)
        return result['data']

    def prepare_request(self,
                        data: Optional[dict],
                        method: RequestMethod) -> tuple[dict, dict]:
        access_token = data.pop('access_token', None)
        if access_token:
            return data, {
                'x-token': access_token
            }
        return data, {}


zuth_service = ZuthService()
