# -*- coding: utf-8 -*-
import json
import random

from django.views import View
from django.views.decorators.csrf import csrf_exempt

from response.response import Response
from verification.request_verify import request_verify
from login.dto import verification_code
from login.service.verification_code_service import VerificationCode


class VerificationCodeView(View):

    # 发送验证码
    @staticmethod
    @request_verify(verification_code.SendCode)
    @csrf_exempt
    def send_code(data_obj):
        response = Response()
        verification_service = VerificationCode()
        res_code, res_data = verification_service.send_code(data_obj.phone)
        return response.response_json(res_code, res_data)

    # 校验 验证码
    @staticmethod
    @request_verify(verification_code.VerCode)
    @csrf_exempt
    def ver_code(data_obj):
        response = Response()
        verification_service = VerificationCode()
        res_code, res_data = verification_service.ver_code(data_obj.phone, data_obj.code)
        return response.response_json(res_code, res_data)
