# -*- coding: utf-8 -*-
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from response.response import Response
from verification.request_verify import request_verify
from order.dto import order
from order.service.order_service import OrderService


class OrderView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # 新增订单（购买）
    @staticmethod
    @request_verify(order.Add)  # 数据校验
    def post(data_obj):
        response = Response()
        merchant_service = OrderService()
        res_code, res_data = merchant_service.add(data_obj)
        return response.response_json(res_code, res_data)

    # 获取订单
    @staticmethod
    @request_verify(order.Inquire)               # 数据校验
    def get(data_obj):
        response = Response()
        merchant_service = OrderService()
        res_code, res_data = merchant_service.inquire(data_obj)
        return response.response_json(res_code, res_data)

    # 修改订单
    @staticmethod
    @request_verify(order.Update)  # 数据校验
    @csrf_exempt
    def put(data_obj):
        response = Response()
        merchant_service = OrderService()
        res_code, res_data = merchant_service.update(data_obj)
        return response.response_json(res_code, res_data)


