# -*- coding: utf-8 -*-
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from response.response import Response
from verification.request_verify import request_verify
from stock.dto import stock
from stock.service.stock_service import StockService


class StockView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # 添加商品
    @staticmethod
    @request_verify(stock.Add)  # 数据校验
    @csrf_exempt
    def post(data_obj):
        response = Response()
        stock_service = StockService()
        res_code, res_data = stock_service.stock_add(data_obj)
        return response.response_json(res_code, res_data)

    # 获取商品
    @staticmethod
    @request_verify(stock.Inquire)               # 数据校验
    def get(data_obj):
        response = Response()
        stock_service = StockService()
        res_code, res_data = stock_service.stock_inquire(data_obj)
        return response.response_json(res_code, res_data)

    # 删除商品
    @staticmethod
    @request_verify(stock.Delete)  # 数据校验
    def delete(data_obj):
        response = Response()
        stock_service = StockService()
        res_code, res_data = stock_service.stock_delete(data_obj)
        return response.response_json(res_code, res_data)

    # 修改商品
    @staticmethod
    @request_verify(stock.Update)  # 数据校验
    @csrf_exempt
    def put(data_obj):
        response = Response()
        stock_service = StockService()
        res_code, res_data = stock_service.stock_update(data_obj)
        return response.response_json(res_code, res_data)

    # 获取sid
    @staticmethod
    @csrf_exempt
    def get_id(req):
        response = Response()
        stock_service = StockService()
        res_code, res_data = stock_service.create_sid()
        return response.response_json(res_code, res_data)

