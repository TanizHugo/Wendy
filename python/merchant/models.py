# -*- coding: utf-8 -*-
from django.db import models

from utils.data_limit import max_length, password_max_length


# 注册人人信息表
class Registrant(models.Model):
    uid = models.CharField(primary_key=True, max_length=max_length, verbose_name='身份证')  # 主键
    phone = models.CharField(max_length=max_length, verbose_name='手机号')
    user_name = models.CharField(max_length=max_length, verbose_name='姓名')

    class Meta:
        db_table = 'registrant'


# 商家数据表
class Merchant(models.Model):
    mid = models.CharField(primary_key=True, max_length=max_length, verbose_name='商家ID')    # 主键
    name = models.CharField(default='', unique=True, max_length=max_length, verbose_name='商家名')
    password = models.CharField(null=False, max_length=password_max_length, verbose_name='密码')
    address = models.CharField(default='', max_length=max_length, verbose_name='地址')
    register_time = models.DateTimeField(auto_now_add=True, verbose_name='注册日期')
    approval = models.BooleanField(default=False, verbose_name='审批通过')
    reason = models.CharField(default='', max_length=max_length, verbose_name='审批原因')

    class Meta:
        db_table = 'merchant'


# 注册人与商家信息关系表
class MerchantRegistrant(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, verbose_name='商家ID')    # 外键
    registrant = models.ForeignKey(Registrant, on_delete=models.CASCADE, verbose_name='注册人ID')   # 外键

    class Meta:
        db_table = 'merchant_registrant'


# 许可码
class License(models.Model):
    code = models.CharField(primary_key=True, max_length=max_length, verbose_name='许可码')  # 主键
    activation_time = models.IntegerField(default=0, verbose_name="激活日期")               # 时间戳
    limit_time = models.IntegerField(default=0, verbose_name="使用期限")                    # 时间戳
    license_state = models.IntegerField(default=2, verbose_name='使用状态')                 # 默认未使用

    class Meta:
        db_table = 'license'


# 商家使用许可码状态
class MerchantLicense(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, verbose_name='商家ID')    # 外键
    license = models.ForeignKey(License, on_delete=models.CASCADE, verbose_name='许可码ID')   # 外键

    class Meta:
        db_table = 'merchant_license'


