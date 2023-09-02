from django.urls import path

from stock.contorller.stock_views import StockView
from stock.contorller.label_views import LabelView

urlpatterns = [
    path('label', LabelView.as_view()),           # 标签的增删查
    path('stock', StockView.as_view()),           # 商品增删改查
    path('getSid', StockView.get_id),             # 获取sid
]