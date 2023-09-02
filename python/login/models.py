# -*- coding: utf-8 -*-
from django.db import models

from utils.data_limit import max_length


# 广告访问数据表
class RequestAdvertise(models.Model):
    openid = models.CharField(max_length=max_length, verbose_name='用户ID')
    req_time = models.IntegerField(verbose_name='点击广告时间')
    aid = models.CharField(max_length=max_length, verbose_name='广告ID')

    class Meta:
        db_table = 'request_ad'


# 用户访问数据表
class RequestUser(models.Model):
    openid = models.CharField(max_length=max_length, verbose_name='用户ID')
    req_time = models.IntegerField(verbose_name='访问时间')

    class Meta:
        db_table = 'request_user'


