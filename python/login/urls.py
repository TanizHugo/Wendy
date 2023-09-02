# -*- coding: utf-8 -*-
from django.urls import path

from login.controller.login_views import LoginView
from login.controller.verification_code_views import VerificationCodeView
from login.controller.request_views import RequestView


urlpatterns = [
    path('comLogin', LoginView.com_login),              # 登陆
    path('vxLogin', LoginView.vx_login),                # 微信登录
    path('sendCode', VerificationCodeView.send_code),   # 注册（发送验证码）
    path('verCode', VerificationCodeView.ver_code),     # 注册（校验验证码）
    path('online', RequestView.get_online_user),        # 获取在线人数
    path('deonline', RequestView.del_online_user),      # 用户退出系统
    path('decodeToken', LoginView.decode_token),        # 解析token
]
