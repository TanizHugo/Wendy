# -*- coding: utf-8 -*-
import os

from django.db import transaction
from django.http import QueryDict

from response.response_obj import ResponseFile
from photo.config.photo_use import *
from photo.models import Pic
from photo.dto.photo_respone_code import PhotoResultCode


class PhotoService(object):

    # 保存图片
    def upload(self, request):
        res_code = None
        res_data = None

        data_dict = request.POST
        _id = data_dict.get('id', None)
        use = pic_path.get(data_dict.get('use', None), None)

        # 判断id是否重复
        try:
            Pic.objects.get(id=_id)
            res_code = PhotoResultCode.EXIST.value          # id重复
            return res_code, res_data
        except:
            pass

        path = os.path.join('/opt', 'pic', use)             # 图片保存路径

        try:
            with transaction.atomic():
                path = self.save_pic(request, path)         # 保存文件

                pic = Pic(
                    id=_id,
                    use=use,
                    path=path,
                )
                pic.save()

                res_code = PhotoResultCode.SUCCESS.value
                res_data = {'path': path}
        except:
            res_code = PhotoResultCode.UPLOAD_ERR.value

        return res_code, res_data

    # 更新图片
    def update(self, request):
        res_code = None
        res_data = None

        data_dict = request.POST
        _id = data_dict.get('id', None)

        # 判断id是否重复
        try:
            pic = Pic.objects.get(id=_id)
            use = pic.use
        except:
            res_code = PhotoResultCode.NOT_EXIST.value      # 图片不存在
            return res_code, res_data

        path = os.path.join('/opt', 'pic', use)             # 图片保存路径

        try:
            with transaction.atomic():
                path = self.save_pic(request, path)         # 保存文件

                old_path = pic.path
                pic.path = path
                pic.save()

                res_code = PhotoResultCode.SUCCESS.value
                res_data = {'path': path}

                if old_path != path:
                    os.remove(old_path)                         # 删除图片
        except:
            res_code = PhotoResultCode.UPLOAD_ERR.value

        return res_code, res_data

    # 删除图片
    def delete(self, id):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        try:
            with transaction.atomic():
                pic = Pic.objects.get(id=id)
                path = pic.path
                os.remove(path)                 # 删除图片
                pic.delete()                    # 删除数据库

                res_code = PhotoResultCode.SUCCESS.value
        except:
            res_code = PhotoResultCode.DELETE_ERR.value

        return res_code, res_data

    # 获取图片
    def inquire(self, data_obj):
        res_code = None
        res = None

        try:
            Pic.objects.get(id=data_obj.id)
            if data_obj.type == 'path':
                res_code, res = self.inquire_path(data_obj.id)
            elif data_obj.type == 'img':
                res_code, res = self.inquire_file(data_obj.id)
        except:
            res_code = PhotoResultCode.NOT_EXIST.value      # 图片不存在

        return res_code, res

    # 获取图片（文件流）
    @staticmethod
    def inquire_file(_id):
        file_obj = ResponseFile()
        try:
            pic = Pic.objects.get(id=_id)
            path = pic.path

            file_name = path.split("\\")[-1]            # 文件名
            suffix = file_name.split('.')[-1].lower()   # 后缀

            file_obj.file_name = file_name
            file_obj.file_path = path

            # 根据文件结尾获取content_type
            if suffix == 'doc':
                file_obj.content_type = 'application/msword'
            elif suffix == 'png':
                file_obj.content_type = 'image/png'
            elif suffix == 'jpg' or suffix == 'jpeg' or suffix == 'jfif':
                file_obj.content_type = 'image/jpeg'

            res_code = PhotoResultCode.SUCCESS.value
        except:
            res_code = PhotoResultCode.INQUIRE_ERR.value
        return res_code, file_obj

    # 获取图片（路径）
    @staticmethod
    def inquire_path(_id):
        res_code = None                     # http 返回码
        res_data = None

        try:
            path = Pic.objects.get(id=_id).path
            res_code = PhotoResultCode.SUCCESS.value
            res_data = {'path': path}
        except:
            res_code = PhotoResultCode.INQUIRE_ERR.value

        return res_code, res_data

    # 保存文件
    @staticmethod
    def save_pic(request, path):
        file_name = None
        print(request.FILES)
        for i in request.FILES:

            file = request.FILES[i]
            if file:
                file_name = os.path.join(path, file.name)
                destination = open(file_name, 'wb+')
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()

        return file_name

