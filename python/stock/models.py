# -*- coding: utf-8 -*-
from django.db import models

from utils.data_limit import max_length
from merchant.models import Merchant


# 商品标签数据表
class Label(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, verbose_name='商家ID')    # 商家 外键
    label_name = models.CharField(max_length=max_length, verbose_name='标签名')

    class Meta:
        db_table = 'label'


# 商品数据表
class Stock(models.Model):
    sid = models.CharField(primary_key=True, max_length=max_length, verbose_name='商品ID')    # 主键
    stock_name = models.CharField(unique=True, max_length=max_length, verbose_name='商品名')
    price = models.FloatField(default=0.0,  verbose_name='价格')
    num = models.IntegerField(default=0, verbose_name='库存数量')
    sold = models.IntegerField(default=0, verbose_name='已售数量')
    type = models.IntegerField(verbose_name='类型')
    flowers = models.CharField(max_length=max_length, verbose_name='主要花材')
    material = models.CharField(max_length=max_length, verbose_name='使用材料')
    package = models.CharField(max_length=max_length, verbose_name='鲜花包装')
    lof = models.CharField(max_length=max_length, verbose_name='花语')

    class Meta:
        db_table = 'stock'


# 商家与商品关系表
class MerchantStock(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, verbose_name='商家ID')    # 商家 外键
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name='商品ID')   # 商品 外键

    class Meta:
        db_table = 'merchant_stock'


# 商品和标签关系表
class StockLabel(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name='商品ID')   # 商品 外键
    label = models.ForeignKey(Label, on_delete=models.CASCADE, verbose_name='标签ID')   # 标签 外键

    class Meta:
        db_table = 'stock_label'

