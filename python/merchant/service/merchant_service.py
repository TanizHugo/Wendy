# -*- coding: utf-8 -*-
import time

from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from merchant.models import Registrant, Merchant, MerchantRegistrant, MerchantLicense, License
from merchant.dto.merchant_respone_code import MerchantResultCode
from merchant.config.license_state import *
from utils.model_control import ModelControl
from utils.generate_uuid import create_fixed_number


class MerchantService(object):

    # 商家添加（註冊）
    def merchant_add(self, data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        # 商鋪名重复检查
        try:
            Merchant.objects.get(name=data_obj.name)
            res_code = MerchantResultCode.NAME_EXIST.value      # 店铺名已经存在
            return res_code, res_data
        except:
            pass

        # 许可码是否存在
        try:
            License.objects.get(code=data_obj.code)
        except:
            res_code = MerchantResultCode.CODE_REE.value        # 许可码错误
            return res_code, res_data


        # 写入数据库
        try:
            with transaction.atomic():
                self.add_model(data_obj)            # 创建用户组表（数据库）
                res_code = MerchantResultCode.SUCCESS.value         # 成功
        except:
            res_code = MerchantResultCode.REGISTER_ERR.value        # 注册失败

        return res_code, res_data

    # 商家查询
    def merchant_inquire(self, data_obj):
        res_code = None                     # http 返回码
        res_data = dict()                   # http 返回数据
        merchants = Merchant.objects.all()  # 查询所有数据

        # 数据存在？
        if not merchants:
            res_code = MerchantResultCode.SUCCESS.value             # 成功
            return res_code, res_data

        try:
            data, res_data['total'] = self.inquire_obj(data_obj)    # 复杂查询
            res_data['data'] = self.data_tidy(data)
            res_code = MerchantResultCode.SUCCESS.value             # 成功
        except:
            res_code = MerchantResultCode.INQUIRE_ERR.value             # 查询失败

        return res_code, res_data

    # 商家刪除
    @staticmethod
    def merchant_delete(data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        # 写入数据库
        try:
            with transaction.atomic():
                merchant = Merchant.objects.get(mid=data_obj.mid)
                MerchantRegistrant.objects.get(merchant=merchant).registrant.delete()
                merchant.delete()
                res_code = MerchantResultCode.SUCCESS.value         # 成功
        except:
            res_code = MerchantResultCode.DELETE_ERR.value          # 删除失败
        return res_code, res_data

    # 商家修改
    def merchant_update(self, data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        # 商家是否存在
        try:
            Merchant.objects.get(mid=data_obj.mid)
        except:
            res_code = MerchantResultCode.NOT_EXIST.value       # 店铺不存在
            return res_code, res_data

        try:
            with transaction.atomic():
                self.update_model(data_obj)
                res_code = MerchantResultCode.SUCCESS.value     # 成功
        except:
            res_code = MerchantResultCode.UPDATE_ERR.value      # 失败
        return res_code, res_data

    # 商家ID生成
    @staticmethod
    def create_mid():
        res_code = None                     # http 返回码
        res_data = dict()                   # http 返回数据
        mid = create_fixed_number(10, 'character')
        if mid:
            res_code = MerchantResultCode.SUCCESS.value
            res_data['mid'] = mid
        else:
            res_code = MerchantResultCode.CREATE_UUID_ERR.value
        return res_code, res_data

    # 审批通过
    @staticmethod
    def merchant_approval_pass(data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据
        try:
            lic = License.objects.get(code=data_obj.code)
            # 许可码状态修改
            lic.activation_time = int(time.time())
            lic.license_state = 1
            lic.save()

            # 商家状态修改
            merchant = MerchantLicense.objects.get(license=lic).merchant
            merchant.approval = True
            merchant.save()

            res_code = MerchantResultCode.SUCCESS.value         # 成功
        except:
            res_code = MerchantResultCode.PASS_ERR.value        # 通过失败
        return res_code, res_data

    # 审批拒绝
    @staticmethod
    def merchant_approval_reject(data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据
        try:
            lic = License.objects.get(code=data_obj.code)
            # 许可码状态修改
            lic.license_state = 3
            lic.save()

            # 商家状态修改
            merchant = MerchantLicense.objects.get(license=lic).merchant
            merchant.approval = False
            merchant.reason = data_obj.reason
            merchant.save()

            res_code = MerchantResultCode.SUCCESS.value          # 成功
        except:
            res_code = MerchantResultCode.REJECT_ERR.value        # 驳回失败
        return res_code, res_data

    # 整理数据（返回）
    @staticmethod
    def data_tidy(merchants):
        res_data = list()
        for merchant in merchants:
            obj = MerchantRegistrant.objects.get(merchant=merchant)
            reg = obj.registrant
            obj = MerchantLicense.objects.get(merchant=merchant)
            lic = obj.license
            res_data.append({
                'mid': merchant.mid,
                'name': merchant.name,
                'address': merchant.address,
                'register_time': merchant.register_time,
                'approval': merchant.approval,
                'reason': merchant.reason,
                'uid': reg.uid,
                'phone': reg.phone,
                'user_name': reg.user_name,
                'limit_time': lic.limit_time,
                'license_state': lic.license_state,
                'activation_time': lic.activation_time,
                'code': lic.code,
                'end_time': lic.limit_time + lic.activation_time,
            })
        return res_data

    # 复杂查询
    @staticmethod
    def inquire_obj(data_obj):
        merchant_obj = list()

        # 分页查询
        page = int(data_obj.page)
        page_size = int(data_obj.page_size)
        start = (page - 1) * page_size
        end = page_size * page

        # 精准查询
        if data_obj.mid or data_obj.name:
            q = Q()
            q.connector = 'OR'
            if data_obj.mid:
                q.children.append(('mid', data_obj.mid))
            elif data_obj.name:
                q.children.append(('name', data_obj.name))
            merchant_obj.append(set(Merchant.objects.filter(q)))

        # 注册码外键查询
        if data_obj.code:
            merchant_lic = MerchantLicense.objects.get(license_id=data_obj.code)
            merchant = merchant_lic.merchant
            merchant_obj.append(set([merchant]))

        # 使用状态 查询
        if data_obj.license_state and int(data_obj.license_state) != UNUSED:
            lic_list = License.objects.filter(license_state=int(data_obj.license_state))
            merchant_obj.append(set([MerchantLicense.objects.get(license=k).merchant for k in lic_list]))

        # 审批通过与否 查询
        if data_obj.approval:
            approval = True if data_obj.approval == 'true' else False
            merchant_obj.append(set(Merchant.objects.filter(approval=approval)))

        # 所有内容
        merchant_obj.append(set(Merchant.objects.all()))

        merchants = list(set.intersection(*[merchant for merchant in merchant_obj]))    # 通过元组 找出同类项

        return merchants[start:end], len(merchants)

    # 外键查询
    def inquire(self, data_obj):
        lic = License.objects.get(code=data_obj.code)
        merchant = MerchantLicense.objects.get(license=lic).merchant
        return merchant

    # 数据表添加
    @staticmethod
    def add_model(data_obj):
        # 密码加密
        data_obj.password = make_password(data_obj.password, None, 'pbkdf2_sha256')

        # 商家数据表
        dict_param = ModelControl.copy_model(Merchant, data_obj)
        merchant = Merchant(**dict_param)
        merchant.save()

        # 注册人人信息表
        dict_param = ModelControl.copy_model(Registrant, data_obj)
        registrant = Registrant(**dict_param)
        registrant.save()

        # 注册人与商家信息关系表
        data_obj.registrant = registrant
        data_obj.merchant = merchant
        dict_param = ModelControl.copy_model(MerchantRegistrant, data_obj)
        merchant_register = MerchantRegistrant(**dict_param)
        merchant_register.save()

        # 商家与许可码的关系表
        lic = License.objects.get(code=data_obj.code)
        lic.license_state = EXPIRED
        data_obj.license = lic
        dict_param = ModelControl.copy_model(MerchantLicense, data_obj)
        merchant_license = MerchantLicense(**dict_param)
        merchant_license.save()

    # 数据表修改
    @staticmethod
    def update_model(data_obj):
        # 用户表的添加
        merchant = Merchant.objects.filter(mid=data_obj.mid)
        dict_param = ModelControl.copy_model(Merchant, data_obj)        # 获取写入表的数据
        merchant.update(**dict_param)                                   # 修改&写入



