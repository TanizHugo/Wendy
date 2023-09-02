# -*- coding: utf-8 -*-
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from response.response import Response
from verification.request_verify import request_verify
from advertise.dto import advertise
from advertise.service.advertise_service import AdvertiseService


class AdvertiseView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # 新增广告
    @staticmethod
    @request_verify(advertise.Add)  # 数据校验
    @csrf_exempt
    def post(data_obj):
        response = Response()
        advertise_service = AdvertiseService()
        res_code, res_data = advertise_service.add(data_obj)
        return response.response_json(res_code, res_data)

    # 获取广告
    @staticmethod
    @request_verify(advertise.Inquire)               # 数据校验
    def get(data_obj):
        response = Response()
        advertise_service = AdvertiseService()
        res_code, res_data = advertise_service.inquire(data_obj)
        return response.response_json(res_code, res_data)

    # 删除广告
    @staticmethod
    @request_verify(advertise.Delete)  # 数据校验
    def delete(data_obj):
        response = Response()
        advertise_service = AdvertiseService()
        res_code, res_data = advertise_service.delete(data_obj)
        return response.response_json(res_code, res_data)

    # 修改广告
    @staticmethod
    @request_verify(advertise.Update)  # 数据校验
    @csrf_exempt
    def put(data_obj):
        response = Response()
        advertise_service = AdvertiseService()
        res_code, res_data = advertise_service.update(data_obj)
        return response.response_json(res_code, res_data)

    # 生成广告id
    @staticmethod
    @csrf_exempt
    def get_id(req):
        response = Response()
        advertise_service = AdvertiseService()
        res_code, res_data = advertise_service.create_code()
        return response.response_json(res_code, res_data)

