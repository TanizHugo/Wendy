# -*- coding: utf-8 -*-
import requests

import jwt
import subprocess
import crypt
from django.contrib.auth.hashers import check_password

from cart.models import ShopCart
from utils.permission import generate_jwt_token
from merchant.models import MerchantRegistrant, Registrant
from login.dto.login_respone_code import LoginResultCode
from login.config.login_identity import *
from utils.permission import UsageStatus
from wendy.settings import APP_ID, APP_Secret
from wendy.settings import SECRET_KEY


# 登录服务
class LoginService(object):

    # 解析token
    @staticmethod
    def decode_token(data_obj):
        res_code = None
        res_data = dict()
        try:
            jwt_dict = jwt.decode(data_obj.token, SECRET_KEY, algorithms=['HS256'])
            res_data['user_name'] = jwt_dict.get('data').get('user_name')
            res_data['role'] = jwt_dict.get('data').get('role')
            res_code = LoginResultCode.SUCCESS.value        # 成功
        except:
            res_code = LoginResultCode.ERR.value            # 失败
        return res_code, res_data

    # 身份验证
    def login(self, data_obj):
        if data_obj.name == 'root':
            return self.root_login_system(data_obj)     # 管理员
        else:
            return self.others_login_system(data_obj)      # 商家或用户

    # root 账号登录验证
    @staticmethod
    def root_login_system(data_obj):
        res_code = None                 # http 返回码
        res_data = dict()               # http 返回数据
        usage = UsageStatus()           # 登录状态

        # user_name = subprocess.check_output(
        #     'cat /etc/shadow | grep {0}'.format(data_obj.name), shell=True)
        #
        # user_name = str(user_name).replace('\n', '')
        # if ':' in user_name:
        #     _pass = user_name.split(':')[1].strip(' ')
        #     salt = _pass[_pass.find('$'):_pass.rfind('$')]
        #     cy = crypt.crypt(data_obj.password, salt)
        if data_obj.name == 'hugo@1024':
            # 生成token
            token = generate_jwt_token(data_obj.name, ADMIN)
            res_code = LoginResultCode.SUCCESS.value
            res_data['token'] = token
            res_data['role'] = ADMIN
            usage.refresh(data_obj.name)                   # 加入监控
        else:
            res_code = LoginResultCode.PASSWORD_ERR.value
        return res_code, res_data

    # 商家账号验证
    @staticmethod
    def others_login_system(data_obj):
        res_code = None             # 返回码
        res_data = dict()           # 返回数据
        usage = UsageStatus()

        try:
            registrant = Registrant.objects.get(uid=data_obj.name)
            merchant = MerchantRegistrant.objects.get(registrant=registrant).merchant

            # 校验密码 和 商家是否通过审批
            if not check_password(data_obj.password, merchant.password):
                res_code = LoginResultCode.PWD_ERR.value            # 密码错误
            elif not merchant.approval:
                res_code = LoginResultCode.APPROVAL_ERR.value       # 商家未通过审核
            else:
                token = generate_jwt_token(data_obj.name, BUS)      # 修改token信息
                res_data['token'] = token
                res_data['role'] = BUS
                res_data['mid'] = merchant.mid
                usage.refresh(data_obj.name)
                res_code = LoginResultCode.SUCCESS.value             # 成功
        except:
            res_code = LoginResultCode.USER_NOT_EXIST.value             # 账号不存在
        return res_code, res_data

    # vx身份验证
    def vx_login(self, login_code):
        res_code = None                 # http 返回码
        res_data = dict()               # http 返回数据
        state, data = self.req_vx_login(login_code)
        # 成功
        if state:
            openid = data
            token = generate_jwt_token(openid, USER)  # 修改token信息
            res_data['token'] = token
            res_data['openid'] = openid
            res_code = LoginResultCode.SUCCESS.value  # 成功
        # 失败
        else:
            err_code = data
            if err_code == '40029':
                res_code = LoginResultCode.VX_40029.value
            elif err_code == '45011':
                res_code = LoginResultCode.VX_45011.value
            elif err_code == '40226':
                res_code = LoginResultCode.VX_40226.value
            elif err_code == '40163':
                res_code = LoginResultCode.VX_40163.value
            elif err_code == '-1':
                res_code = LoginResultCode.VX_1.value
            else:
                res_code = LoginResultCode.LOGIN_ERR.value

        return res_code, res_data

    # 请求vx登录验证接口
    def req_vx_login(self, login_code):
        response = requests.get(
            "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code"
            % (APP_ID, APP_Secret, login_code))

        result = response.json()
        if 'errcode' in result.keys():
            res_data = result.get('errcode', None)
            state = False
        else:
            res_data = result.get('openid', None)
            # 首次登录创建购物车
            self.create_user_cart(res_data)

            state = True
        return state, res_data

    # 创建购物车
    @staticmethod
    def create_user_cart(openid):
        try:
            ShopCart.objects.get(openid=openid)
        except:
            cart = ShopCart(openid=openid)
            cart.save()


