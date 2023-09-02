# -*- coding: utf-8 -*-
from django.urls import path

from order.contorller.order_view import OrderView

urlpatterns = [
    path('order', OrderView.as_view()),    # 订单的增改查
]
