# -*- coding: utf-8 -*-
from django.urls import path

from photo.controller.photo_view import PhotoView

urlpatterns = [
    path('photo', PhotoView.as_view()),              # 图片增删查
    path('updatePhoto', PhotoView.update)            # 图片改
]


