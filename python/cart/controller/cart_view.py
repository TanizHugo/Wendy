# -*- coding: utf-8 -*-
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from response.response import Response
from verification.request_verify import request_verify
from cart.dto import cart
from cart.service.cart_service import CartService


class MerchantView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # 获取购物车
    @staticmethod
    @request_verify(cart.InquireCart)               # 数据校验
    def get(data_obj):
        response = Response()
        cart_service = CartService()
        res_code, res_data = cart_service.cart_inquire(data_obj)
        return response.response_json(res_code, res_data)

    # 批量删除购物车内容
    @staticmethod
    @request_verify(cart.DeleteCart)               # 数据校验
    def delete(data_obj):
        response = Response()
        cart_service = CartService()
        res_code, res_data = cart_service.cart_delete(data_obj)
        return response.response_json(res_code, res_data)

    # 修改购物车
    @staticmethod
    @request_verify(cart.UpdateCart)  # 数据校验
    @csrf_exempt
    def put(data_obj):
        response = Response()
        cart_service = CartService()
        res_code, res_data = cart_service.cart_update(data_obj)
        return response.response_json(res_code, res_data)

    # 购物车商品选购数量修改
    @staticmethod
    @request_verify(cart.UpdateCartNum)  # 数据校验
    @csrf_exempt
    def cart_num(data_obj):
        response = Response()
        cart_service = CartService()
        res_code, res_data = cart_service.cart_stock_num_update(data_obj)
        return response.response_json(res_code, res_data)

    # 审批拒绝
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

