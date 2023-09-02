# -*- coding: utf-8 -*-

from django.db import transaction
from django.db.models import Q

from stock.models import Stock, MerchantStock, Merchant, Label
from stock.dto.stok_respone_code import StockResultCode
from utils.model_control import ModelControl


class LabelService(object):

    # 标签添加
    def label_add(self, data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        # 商鋪名重复检查
        try:
            merchant = Merchant.objects.get(mid=data_obj.mid)
            Label.objects.get(merchant=merchant, label_name=data_obj.label_name)
            res_code = StockResultCode.LABEL_NAME_EXIST.value      # 标签名已经存在
            return res_code, res_data
        except:
            pass

        # 写入数据库
        try:
            with transaction.atomic():
                self.add_model(data_obj)            # 创建用户组表（数据库）
                res_code = StockResultCode.SUCCESS.value         # 成功
        except:
            res_code = StockResultCode.ADD_ERR.value        # 添加失败

        return res_code, res_data

    # 标签查询
    def label_inquire(self, data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据
        merchant = Merchant.objects.get(mid=data_obj.mid)
        labels = Label.objects.filter(merchant=merchant)

        data_obj.merchant = merchant
        # 数据存在？
        if not labels:
            res_code = StockResultCode.SUCCESS.value             # 成功
            return res_code, res_data
        try:
            res_data = self.data_tidy(labels)
            res_code = StockResultCode.SUCCESS.value             # 成功
        except:
            res_code = StockResultCode.INQUIRE_ERR.value         # 查询失败

        return res_code, res_data

    # 标签刪除
    @staticmethod
    def label_delete(data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        # 写入数据库
        try:
            with transaction.atomic():
                merchant = Merchant.objects.get(mid=data_obj.mid)
                Label.objects.get(merchant=merchant, label_name=data_obj.label_name).delete()
                res_code = StockResultCode.SUCCESS.value         # 成功
        except:
            res_code = StockResultCode.DELETE_ERR.value          # 删除失败
        return res_code, res_data

    # 整理数据（返回）
    @staticmethod
    def data_tidy(data):
        res_data = list()
        for ra in data:
            res_data.append(ra.label_name)
        return res_data

    # 数据表添加
    @staticmethod
    def add_model(data_obj):
        # 商品数据表
        data_obj.merchant = Merchant.objects.get(mid=data_obj.mid)
        dict_param = ModelControl.copy_model(Label, data_obj)
        label = Label(**dict_param)
        label.save()


