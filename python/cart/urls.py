# -*- coding: utf-8 -*-
from django.urls import path

from cart.contorller.cart_view import CartView

urlpatterns = [
    path('cart', CartView.as_view()),                           # 购物车的增删改查
    path('updateCartStockNum', CartView.cart_stock_num),        # 更新购物车商品数量
    path('updateCartAllState', CartView.all_state),             # 修改购物车全选状态
    path('updateCartState', CartView.stock_state),              # 修改购物车单个选中状态
]