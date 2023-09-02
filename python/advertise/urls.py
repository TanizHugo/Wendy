# -*- coding: utf-8 -*-
from django.urls import path

from advertise.contorller.advertise_view import AdvertiseView

urlpatterns = [
    path('advertise', AdvertiseView.as_view()),           # 广告增删改查
    path('getAid', AdvertiseView.get_id),                 # 获取广告编号
]