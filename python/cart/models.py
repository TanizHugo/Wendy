# -*- coding: utf-8 -*-
from django.db import models

from utils.data_limit import max_length
from stock.models import Stock


# 购物车数据表
class ShopCart(models.Model):
    openid = models.CharField(primary_key=True, max_length=max_length, verbose_name='用户ID')    # 主键
    total_money = models.FloatField(default=0.0, verbose_name='购物车总价')
    select_money = models.FloatField(default=0.0, verbose_name='选中物件价格')
    num = models.IntegerField(default=0, verbose_name='购物车总数量')
    select_all = models.BooleanField(default=False, verbose_name='是否全选')

    class Meta:
        db_table = 'shop_cart'


# 购物车购买商品内容
class CartStock(models.Model):
    shop_cart = models.ForeignKey(ShopCart, on_delete=models.CASCADE, verbose_name='购物车ID')  # 商家商 外键
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name='商品ID')  # 商家商 外键
    quantity = models.IntegerField(verbose_name='购买数量')
    select_state = models.BooleanField(default=False, verbose_name='是否选中')
    paid = models.BooleanField(default=False, verbose_name='是否支付')

    class Meta:
        db_table = 'cart_stock'


