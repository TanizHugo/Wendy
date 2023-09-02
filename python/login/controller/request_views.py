# -*- coding: utf-8 -*-
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from login.service.request_service import RequestService
from response.response import Response
from verification.request_verify import request_verify
from login.dto import request


class RequestView(View):

    @staticmethod
    @csrf_exempt
    def get_online_user(req):
        response = Response()
        request_service = RequestService()
        res_code, res_data = request_service.get_online_num()
        return response.response_json(res_code, res_data)

    @staticmethod
    @request_verify(request.DeleteOnlineUser)                # 数据校验
    @csrf_exempt
    def del_online_user(data_obj):
        response = Response()
        request_service = RequestService()
        res_code, res_data = request_service.del_online_user(data_obj)
        return response.response_json(res_code, res_data)
