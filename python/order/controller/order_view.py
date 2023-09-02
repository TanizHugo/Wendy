# -*- coding: utf-8 -*-
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from response.response import Response
from verification.request_verify import request_verify
from order.dto import order
from order.service.order_service import OrderService


class MerchantView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # 新增订单（购买）
    @staticmethod
    @request_verify(order.AddSingleOrder)  # 数据校验
    @csrf_exempt
    def single_order(data_obj):
        response = Response()
        merchant_service = OrderService()
        res_code, res_data = merchant_service.order_single_add(data_obj)
        return response.response_json(res_code, res_data)

    # 新增订单（结算购物车）
    @staticmethod
    @request_verify(order.AddCartOrder)  # 数据校验
    @csrf_exempt
    def cart_order(data_obj):
        response = Response()
        merchant_service = OrderService()
        res_code, res_data = merchant_service.order_cart_add(data_obj)
        return response.response_json(res_code, res_data)

    # 获取订单
    @staticmethod
    @request_verify(order.InquireOrder)               # 数据校验
    def get(data_obj):
        response = Response()
        merchant_service = OrderService()
        res_code, res_data = merchant_service.order_inquire(data_obj)
        return response.response_json(res_code, res_data)

    # 修改订单
    @staticmethod
    @request_verify(order.UpdateOrder)  # 数据校验
    @csrf_exempt
    def put(data_obj):
        response = Response()
        merchant_service = OrderService()
        res_code, res_data = merchant_service.order_update(data_obj)
        return response.response_json(res_code, res_data)

    # 获取oid
    @staticmethod
    @csrf_exempt
    def get_id(req):
        response = Response()
        merchant_service = OrderService()
        res_code, res_data = merchant_service.create_mid()
        return response.response_json(res_code, res_data)
