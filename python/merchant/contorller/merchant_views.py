# -*- coding: utf-8 -*-
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from response.response import Response
from verification.request_verify import request_verify
from merchant.dto import merchant
from merchant.service.merchant_service import MerchantService


class MerchantView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # 添加商户（注册）
    @staticmethod
    @request_verify(merchant.Add)  # 数据校验
    @csrf_exempt
    def register(data_obj):
        response = Response()
        merchant_service = MerchantService()
        res_code, res_data = merchant_service.merchant_add(data_obj)
        return response.response_json(res_code, res_data)

    # 获取商户
    @staticmethod
    @request_verify(merchant.Inquire)               # 数据校验
    def get(data_obj):
        response = Response()
        merchant_service = MerchantService()
        res_code, res_data = merchant_service.merchant_inquire(data_obj)
        return response.response_json(res_code, res_data)

    # 删除商户
    @staticmethod
    @request_verify(merchant.Delete)  # 数据校验
    def delete(data_obj):
        response = Response()
        merchant_service = MerchantService()
        res_code, res_data = merchant_service.merchant_delete(data_obj)
        return response.response_json(res_code, res_data)

    # 修改商户
    @staticmethod
    @request_verify(merchant.Update)  # 数据校验
    @csrf_exempt
    def put(data_obj):
        response = Response()
        merchant_service = MerchantService()
        res_code, res_data = merchant_service.merchant_update(data_obj)
        return response.response_json(res_code, res_data)

    # 获取mid
    @staticmethod
    @csrf_exempt
    def get_id(req):
        response = Response()
        merchant_service = MerchantService()
        res_code, res_data = merchant_service.create_mid()
        return response.response_json(res_code, res_data)

    # 审批通过
    @staticmethod
    @request_verify(merchant.Pass)  # 数据校验
    @csrf_exempt
    def approval_pass(data_obj):
        response = Response()
        merchant_service = MerchantService()
        res_code, res_data = merchant_service.merchant_approval_pass(data_obj)
        return response.response_json(res_code, res_data)

    # 审批拒绝
    @staticmethod
    @request_verify(merchant.Reject)  # 数据校验
    @csrf_exempt
    def approval_reject(data_obj):
        response = Response()
        merchant_service = MerchantService()
        res_code, res_data = merchant_service.merchant_approval_reject(data_obj)
        return response.response_json(res_code, res_data)