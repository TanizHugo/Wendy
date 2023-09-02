# -*- coding: utf-8 -*-
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from response.response import Response
from verification.request_verify import request_verify
from merchant.dto import license
from merchant.service.license_service import LicenseService


class LicenseView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #
    @staticmethod
    @request_verify(license.Add)  # 数据校验
    @csrf_exempt
    def post(data_obj):
        response = Response()
        license_service = LicenseService()
        res_code, res_data = license_service.license_add(data_obj)
        return response.response_json(res_code, res_data)

    # 获取商户
    @staticmethod
    @request_verify(license.Inquire)               # 数据校验
    def get(data_obj):
        response = Response()
        license_service = LicenseService()
        res_code, res_data = license_service.license_inquire(data_obj)
        return response.response_json(res_code, res_data)

    # 删除商户
    @staticmethod
    @request_verify(license.Delete)  # 数据校验
    def delete(data_obj):
        response = Response()
        license_service = LicenseService()
        res_code, res_data = license_service.license_delete(data_obj)
        return response.response_json(res_code, res_data)

    # 修改商户
    @staticmethod
    @request_verify(license.Update)  # 数据校验
    @csrf_exempt
    def put(data_obj):
        response = Response()
        license_service = LicenseService()
        res_code, res_data = license_service.license_update(data_obj)
        return response.response_json(res_code, res_data)

    # 生成许可码
    @staticmethod
    @csrf_exempt
    def get_id(req):
        response = Response()
        license_service = LicenseService()
        res_code, res_data = license_service.create_code()
        return response.response_json(res_code, res_data)

