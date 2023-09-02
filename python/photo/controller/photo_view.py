# -*- coding: utf-8 -*-
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from response.response import Response
from verification.request_verify import request_verify
from photo.service.photo_service import PhotoService
from photo.dto import photo


class PhotoView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # 上传图片
    @staticmethod
    def post(request):
        response = Response()
        photo_service = PhotoService()
        res_code, res_data = photo_service.upload(request)
        return response.response_json(res_code, res_data)

    # 删除图片
    @staticmethod
    @request_verify(photo.Delete)
    def delete(data_obj):
        response = Response()
        photo_service = PhotoService()
        res_code, res_data = photo_service.delete(data_obj.id)
        return response.response_json(res_code, res_data)

    # 获取图片
    @staticmethod
    @request_verify(photo.Inquire)
    def get(data_obj):
        response = Response()
        photo_service = PhotoService()
        _type = data_obj.type
        res_code, res = photo_service.inquire(data_obj)

        if _type == 'path' or res is None:
            return response.response_json(res_code, res)
        elif _type == 'img':
            return response.response_file(res)

    # 修改图片
    @staticmethod
    @csrf_exempt
    def update(request):
        response = Response()
        photo_service = PhotoService()
        res_code, res_data = photo_service.update(request)
        return response.response_json(res_code, res_data)
