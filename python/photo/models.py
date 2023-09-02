# -*- coding: utf-8 -*-
from django.db import models
from utils.data_limit import max_length


# 图片表
class Pic(models.Model):
    id = models.CharField(primary_key=True, max_length=max_length, verbose_name='唯一编号')
    use = models.CharField(max_length=max_length, verbose_name='用途')
    path = models.CharField(max_length=max_length, verbose_name='图片路径')

    class Meta:
        db_table = 'pic'
