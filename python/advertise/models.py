# -*- coding: utf-8 -*-
from django.db import models

from utils.data_limit import max_length, password_max_length


# 广告数据表
class Advertise(models.Model):
    aid = models.CharField(primary_key=True, max_length=max_length, verbose_name='广告ID')  # 主键
    contract = models.CharField(unique=True, max_length=max_length, verbose_name='合同编号')
    source = models.CharField(default='', max_length=max_length, verbose_name='广告来源')
    illustrate = models.CharField(default='', max_length=max_length, verbose_name='广告说明')
    principal = models.CharField(default='', max_length=max_length, verbose_name='负责人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'advertise'


