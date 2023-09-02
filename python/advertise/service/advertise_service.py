# -*- coding: utf-8 -*-
from django.db.models import Q
from django.db import transaction

from advertise.models import Advertise
from advertise.dto.advertise_respone_code import AdvertiseResultCode
from utils.model_control import ModelControl
from utils.generate_uuid import create_fixed_number


class AdvertiseService(object):

    # 许可码添加
    @staticmethod
    def add(data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        # 商鋪名重复检查
        try:
            Advertise.objects.get(aid=data_obj.aid)
            res_code = AdvertiseResultCode.NAME_EXIST.value      # 店铺名已经存在
            return res_code, res_data
        except:
            pass

        # 写入数据库
        try:
            with transaction.atomic():
                ad = Advertise(
                    aid=data_obj.aid,
                    contract=data_obj.contract,
                    source=data_obj.source,
                    illustrate=data_obj.illustrate,
                    principal=data_obj.principal,
                )
                ad.save()
                res_code = AdvertiseResultCode.SUCCESS.value          # 成功
        except Exception as e:
            print(e)
            res_code = AdvertiseResultCode.ADD_ERR.value              # 失败

        return res_code, res_data

    # 商家查询
    def inquire(self, data_obj):
        res_code = None                     # http 返回码
        res_data = dict()                   # http 返回数据
        try:
            ad = Advertise.objects.all()           # 查询所有数据
        except:
            res_code = AdvertiseResultCode.SUCCESS.value             # 成功
            return res_code, res_data

        # 查询数据表数据
        try:
            data, res_data['total'] = self.inquire_obj(data_obj)        # 复杂查询
            res_data['data'] = self.data_tidy(data)
            res_code = AdvertiseResultCode.SUCCESS.value             # 成功
        except:
            res_code = AdvertiseResultCode.INQUIRE_ERR.value             # 查询失败

        return res_code, res_data

    # 商家刪除
    @staticmethod
    def delete(data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        # 写入数据库
        try:
            with transaction.atomic():
                for aid in data_obj.aid_list:
                    Advertise.objects.get(aid=aid).delete()
                res_code = AdvertiseResultCode.SUCCESS.value         # 成功
        except:
            res_code = AdvertiseResultCode.DELETE_ERR.value          # 删除失败
        return res_code, res_data

    # 商家修改
    def update(self, data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        try:
            Advertise.objects.get(aid=data_obj.aid)
        except:
            res_code = AdvertiseResultCode.NAME_NOT_EXIST.value       # 许可码不存在
            return res_code, res_data

        try:
            with transaction.atomic():
                self.update_model(data_obj)
                res_code = AdvertiseResultCode.SUCCESS.value          # 成功
        except:
            res_code = AdvertiseResultCode.UPDATE_ERR.value           # 修改失败
        return res_code, res_data

    # 生成aid
    @staticmethod
    def create_code():
        res_code = None                     # http 返回码
        res_data = dict()                   # http 返回数据
        aid = create_fixed_number(18, 'character')
        if aid:
            res_code = AdvertiseResultCode.SUCCESS.value              # 成功
            res_data['aid'] = aid
        else:
            res_code = AdvertiseResultCode.CREATE_SID_ERR.value      # 广告编号生成失败
        return res_code, res_data

    # 整理数据（返回）
    @staticmethod
    def data_tidy(data):
        res_data = list()
        for ra in data:
            res_data.append({
                'aid': ra.aid,
                'contract': ra.contract,
                'illustrate': ra.illustrate,
                'source': ra.source,
                'principal': ra.principal,
                'create_time': ra.create_time,
            })
        return res_data

    # 复杂查询
    @staticmethod
    def inquire_obj(data_obj):
        q = Q()

        if data_obj.aid:
            q.children.append(('aid', data_obj.aid))
            res = Advertise.objects.filter(q)
            total = 1
        else:
            page = int(data_obj.page)
            page_size = int(data_obj.page_size)
            start = (page - 1) * page_size
            end = page_size * page

            res = Advertise.objects.all()[start:end]
            total = Advertise.objects.all().count()
        return res, total

    # 数据表修改
    @staticmethod
    def update_model(data_obj):
        # 用户表的添加
        ad = Advertise.objects.filter(aid=data_obj.aid)
        dict_param = ModelControl.copy_model(Advertise, data_obj)        # 获取写入表的数据
        ad.update(**dict_param)                                       # 修改&写入
