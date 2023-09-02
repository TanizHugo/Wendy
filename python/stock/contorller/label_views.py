# -*- coding: utf-8 -*-
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from response.response import Response
from verification.request_verify import request_verify
from stock.dto import label
from stock.service.label_service import LabelService


class LabelView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # 添加标签
    @staticmethod
    @request_verify(label.Add)                  # 数据校验
    @csrf_exempt
    def post(data_obj):
        response = Response()
        label_service = LabelService()
        res_code, res_data = label_service.label_add(data_obj)
        return response.response_json(res_code, res_data)

    # 获取标签
    @staticmethod
    @request_verify(label.Inquire)               # 数据校验
    def get(data_obj):
        response = Response()
        label_service = LabelService()
        res_code, res_data = label_service.label_inquire(data_obj)
        return response.response_json(res_code, res_data)

    # 删除标签
    @staticmethod
    @request_verify(label.Delete)  # 数据校验
    def delete(data_obj):
        response = Response()
        label_service = LabelService()
        res_code, res_data = label_service.label_delete(data_obj)
        return response.response_json(res_code, res_data)


