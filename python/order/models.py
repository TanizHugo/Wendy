# -*- coding: utf-8 -*-
from django.db import models

from utils.data_limit import max_length
from stock.models import Stock


# 订单信息数据表
class Order(models.Model):
    oid = models.CharField(primary_key=True, max_length=max_length, verbose_name='订单ID')    # 主键
    openid = models.CharField(max_length=max_length, verbose_name='下单用户')
    state = models.IntegerField(verbose_name='订单状态')
    finish_time = models.IntegerField(default=0, verbose_name='完成订单时间')           # 时间戳
    book_time = models.IntegerField(default=0, verbose_name='预约取件时间')             # 时间戳
    user_name = models.CharField(max_length=max_length, verbose_name='收货人名字')
    phone = models.CharField(max_length=max_length, verbose_name='手机号')
    way = models.CharField(max_length=max_length, verbose_name='收货方式')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'order_table'


# 订单购物内容
class OrderStock(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单ID')   # 订单信息 外键
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name='订单购买内容')   # 商品 外键
    quantity = models.IntegerField(verbose_name='购买数量')
    pay = models.FloatField(verbose_name='付款金额')

    class Meta:
        db_table = 'order_stock'

