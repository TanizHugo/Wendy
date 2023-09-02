# -*- coding: utf-8 -*-
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from response.response import Response
from verification.request_verify import request_verify
from login.dto import login
from login.service.login_service import LoginService


class LoginView(View):

    @staticmethod
    @request_verify(login.Login)  # 数据校验
    @csrf_exempt
    def com_login(data_obj):
        response = Response()
        login_service = LoginService()
        res_code, res_data = login_service.login(data_obj)
        return response.response_json(res_code, res_data)

    @staticmethod
    @request_verify(login.VXLogin)  # 数据校验
    @csrf_exempt
    def vx_login(data_obj):
        response = Response()
        login_service = LoginService()
        res_code, res_data = login_service.vx_login(data_obj.login_code)
        return response.response_json(res_code, res_data)

    @staticmethod
    @request_verify(login.DecodeToken)  # 数据校验
    @csrf_exempt
    def decode_token(data_obj):
        response = Response()
        login_service = LoginService()
        res_code, res_data = login_service.decode_token(data_obj)
        return response.response_json(res_code, res_data)
