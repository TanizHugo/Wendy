# -*- coding: utf-8 -*-
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from response.response import Response
from verification.request_verify import request_verify
from cart.dto import cart
from cart.service.cart_service import CartService


class CartView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # 获取购物车
    @staticmethod
    @request_verify(cart.Inquire)               # 数据校验
    def get(data_obj):
        response = Response()
        cart_service = CartService()
        res_code, res_data = cart_service.inquire(data_obj)
        return response.response_json(res_code, res_data)

    # 批量删除购物车内容
    @staticmethod
    @request_verify(cart.Delete)               # 数据校验
    def delete(data_obj):
        response = Response()
        cart_service = CartService()
        res_code, res_data = cart_service.delete(data_obj)
        return response.response_json(res_code, res_data)

    # 添加购物车
    @staticmethod
    @request_verify(cart.Add)  # 数据校验
    def post(data_obj):
        response = Response()
        cart_service = CartService()
        res_code, res_data = cart_service.add(data_obj)
        return response.response_json(res_code, res_data)

    # 更新购物车商品数量
    @staticmethod
    @request_verify(cart.UpdateCartNum)  # 数据校验
    @csrf_exempt
    def cart_stock_num(data_obj):
        response = Response()
        cart_service = CartService()
        res_code, res_data = cart_service.cart_stock_num_update(data_obj)
        return response.response_json(res_code, res_data)

    # 购物车全选
    @staticmethod
    @request_verify(cart.UpdateCartAllState)  # 数据校验
    @csrf_exempt
    def all_state(data_obj):
        response = Response()
        cart_service = CartService()
        res_code, res_data = cart_service.cart_all_state_update(data_obj)
        return response.response_json(res_code, res_data)

    # 购物车商品选购数量修改
    @staticmethod
    @request_verify(cart.UpdateCartStockState)  # 数据校验
    @csrf_exempt
    def stock_state(data_obj):
        response = Response()
        cart_service = CartService()
        res_code, res_data = cart_service.cart_stock_state_update(data_obj)
        return response.response_json(res_code, res_data)

