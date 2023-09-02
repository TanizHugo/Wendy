# -*- coding: utf-8 -*-
import jwt
from datetime import datetime, timedelta

from wendy.settings import cache
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from wendy.settings import SECRET_KEY
from login.service.request_service import UsageStatus, RequestService
from wendy.command import isRunServer


auth_url_whitelist = ["/login", "/online", "/delonline", "/machine_info", "/admin/uploadPhoto",
                      "/admin/inquirePhoto", "/admin/deletePhoto", "/photo", "/updatePhoto",
                      "/comLogin", ]

auth_url_whitelist1 = ["/comLogin", "/vxLogin", "/register", "/getMid", "/verCode", "/sendCode", "/license"]


# 生成token
def generate_jwt_token(user_name, role):
    token = jwt.encode({
        'exp': datetime.utcnow() + timedelta(days=7),       # 创建一个过期时间
        'iat': datetime.utcnow(),       # 创建时间
        # 用户信息
        'data': {
            'user_name': user_name,
            'role': role,
        }
    },
        # 密匙
        SECRET_KEY,
        algorithm='HS256')

    return token


# 认证
class AuthPermissionRequired(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        if request.path not in auth_url_whitelist1:
            try:
                auth = request.META.get('HTTP_AUTHORIZATION').split()
            except AttributeError:
                return JsonResponse({"code": 401, "message": "没有验证头"})
            token = auth[0]
            # 用户通过API获取数据验证流程
            if token:
                try:
                    request_service = RequestService()

                    # token内容
                    jwt_dict = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                    user_name = jwt_dict.get('data').get('user_name')

                    # # 写入用户名
                    # cache.set(key='current_user', value=user_name)

                    # 用户进行在线状态刷新
                    usage = UsageStatus()
                    usage.refresh(user_name)
                    request_service.add_user_db(user_name)          # 记录数据库

                    # 广告点击次数
                    if request.path == '/clickAd':
                        request_service.add_ad_db(user_name, request)   # 记录数据库

                except jwt.ExpiredSignatureError:
                    return JsonResponse({"status_code": 401, "message": "Token过期"})
                except jwt.InvalidTokenError:
                    return JsonResponse({"status_code": 401, "message": "Token无效"})
                except Exception as e:
                    return JsonResponse(eval(str(e)))
            else:
                return JsonResponse({"status_code": 401, "message": "不支持身份验证类型"})


if isRunServer():
    cache.set(key='usage', value=list())
