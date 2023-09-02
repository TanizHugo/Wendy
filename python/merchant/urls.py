from django.urls import path

from merchant.contorller.merchant_views import MerchantView
from merchant.contorller.licnese_view import LicenseView

urlpatterns = [
    path('merchant', MerchantView.as_view()),           # 商家删改查
    path('register', MerchantView.register),            # 注册
    path('license', LicenseView.as_view()),             # 许可码增删改查
    path('getLic', LicenseView.get_id),                 # 获取许可码
    path('getMid', MerchantView.get_id),                # 获取mid
    path('pass', MerchantView.approval_pass),           # 审批通过
    path('reject', MerchantView.approval_reject),       # 审批驳回
]