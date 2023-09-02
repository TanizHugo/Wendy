# -*- coding: utf-8 -*-

from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from merchant.models import License
from merchant.dto.license_respone_code import LicenseResultCode
from utils.model_control import ModelControl
from utils.generate_uuid import create_fixed_number


class LicenseService(object):

    # 许可码添加
    @staticmethod
    def license_add(data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        # 商鋪名重复检查
        try:
            License.objects.get(code=data_obj.code)
            res_code = LicenseResultCode.NAME_EXIST.value      # 店铺名已经存在
            return res_code, res_data
        except:
            pass

        # 写入数据库
        try:
            with transaction.atomic():
                lic = License(code=data_obj.code, limit_time=data_obj.limit_time)
                lic.save()
                res_code = LicenseResultCode.SUCCESS.value          # 成功
        except:
            res_code = LicenseResultCode.ADD_ERR.value              # 失败

        return res_code, res_data

    # 许可码查询
    def license_inquire(self, data_obj):
        res_code = None                     # http 返回码
        res_data = dict()                   # http 返回数据
        try:
            pic = License.objects.all()           # 查询所有数据
        except:
            res_code = LicenseResultCode.SUCCESS.value             # 成功
            return res_code, res_data

        # 查询数据表数据
        try:
            data, res_data['total'] = self.inquire_obj(data_obj)        # 复杂查询
            res_data['data'] = self.data_tidy(data)
            res_code = LicenseResultCode.SUCCESS.value             # 成功
        except:
            res_code = LicenseResultCode.INQUIRE_ERR.value             # 查询失败

        return res_code, res_data

    # 许可码刪除
    @staticmethod
    def license_delete(data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        # 写入数据库
        try:
            with transaction.atomic():
                merchant = License.objects.get(code=data_obj.code)
                merchant.delete()
                res_code = LicenseResultCode.SUCCESS.value         # 成功
        except:
            res_code = LicenseResultCode.DELETE_ERR.value          # 删除失败
        return res_code, res_data

    # 许可码修改
    def license_update(self, data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        try:
            License.objects.get(code=data_obj.code)
        except:
            res_code = LicenseResultCode.NAME_NOT_EXIST.value       # 许可码不存在
            return res_code, res_data

        try:
            with transaction.atomic():
                self.update_model(data_obj)
                res_code = LicenseResultCode.SUCCESS.value          # 成功
        except:
            res_code = LicenseResultCode.UPDATE_ERR.value           # 修改失败
        return res_code, res_data

    # License code 生成
    @staticmethod
    def create_code():
        res_code = None                     # http 返回码
        res_data = dict()                   # http 返回数据
        code = create_fixed_number(18, 'character')
        if code:
            res_code = LicenseResultCode.SUCCESS.value              # 成功
            res_data['code'] = code
        else:
            res_code = LicenseResultCode.CREATE_CODE_ERR.value      # 许可码生成失败
        return res_code, res_data

    # 整理数据（返回）
    @staticmethod
    def data_tidy(data):
        res_data = list()
        for ra in data:
            res_data.append({
                'code': ra.code,
                'activation_time': ra.activation_time,
                'limit_time': ra.limit_time,
                'license_state': ra.license_state,
                'end_time': ra.limit_time + ra.activation_time,
            })
        return res_data

    # 复杂查询
    @staticmethod
    def inquire_obj(data_obj):
        q = Q()
        q.connector = 'AND'             # q对象表示‘AND’关系，也就是说q下的条件都要满足‘AND’

        page = int(data_obj.page)
        page_size = int(data_obj.page_size)
        start = (page - 1) * page_size
        end = page_size * page

        if data_obj.code:
            q.children.append(('code', data_obj.code))
        elif data_obj.license_state:
            q.children.append(('license_state', data_obj.license_state))

        res = License.objects.filter(q)[start:end]
        total = License.objects.filter(q).count()

        print('res:{}\n totoal:{}'.format(res, total))
        return res, total

    # 数据表修改
    @staticmethod
    def update_model(data_obj):
        # 用户表的添加
        lic = License.objects.filter(code=data_obj.code)
        dict_param = ModelControl.copy_model(License, data_obj)        # 获取写入表的数据
        lic.update(**dict_param)                                       # 修改&写入
