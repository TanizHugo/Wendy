# -*- coding: utf-8 -*-
import json

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import sms_client, models

from wendy.settings import cache
from wendy.settings import SMS_SDK_ID, TEMPLATE_ID, TIME_LIMIT, TX_SECRET_ID, TX_SECRET_KEY
from login.dto.login_respone_code import LoginResultCode
from utils.generate_uuid import create_fixed_number


class VerificationCode(object):

    # 发送验证码
    @staticmethod
    def send_code(phone):
        res_code = None         # http 返回码
        res_data = None         # http 返回数据

        code = create_fixed_number(6, 'number')

        sms = SMS()
        state = sms.send_message(phone, code)   # 发送验证码
        if state:
            res_code = LoginResultCode.SUCCESS.value     # 成功发送
            cache.set(key=phone, value=code)             # 存入cache
        else:
            res_code = LoginResultCode.SEND_CODE_ERR.value   # 成功失败
        return res_code, res_data

    # 校验 验证码
    @staticmethod
    def ver_code(phone, code):
        res_code = None         # http 返回码
        res_data = None         # http 返回数据
        try:
            _code = cache.get(key=phone)    # 获取cache缓存的验证码
        except:
            res_code = LoginResultCode.VER_CODE_EXPIRED.value   # 验证码过期
            return res_code, res_data

        if _code != code:
            res_code = LoginResultCode.VER_CODE_ERR.value       # 验证失败
        else:
            res_code = LoginResultCode.SUCCESS.value            # 成功
            cache.delete(key=phone, version=None)               # 删除一个key
        return res_code, res_data


# 利用腾讯服务实现的验证码发送模块
class SMS(object):

    # 初始化服务（慎重改）
    def __init__(self):
        try:
            cred = credential.Credential(TX_SECRET_ID, TX_SECRET_KEY)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "sms.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            self.client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            self.req = models.SendSmsRequest()
        except TencentCloudSDKException as err:
            print(err)

    # 发送短信
    def send_message(self, phone_num, v_code):

        # 手机号码格式
        if not phone_num.startswith('+86'):
            phone_num = '+86' + str(phone_num)

        params = {
            "PhoneNumberSet": [phone_num],  # 手机号
            "SmsSdkAppId": SMS_SDK_ID,
            "SignName": "娜娜起名困难症公众号",
            "TemplateId": TEMPLATE_ID,
            "TemplateParamSet": [
                v_code,  # 验证码
                TIME_LIMIT,  # 时间限制
            ],
            "SessionContext": "wendy",
        }
        try:
            # 实例化一个请求对象,每个接口都会对应一个request对象
            self.req = models.SendSmsRequest()
            self.req.from_json_string(json.dumps(params))

            # 返回的resp是一个SendSmsResponse的实例，与请求对象对应
            resp = self.client.SendSms(self.req)
            # 输出json格式的字符串回包
            print(resp.to_json_string())
            return True

        except TencentCloudSDKException as err:
            print(err)
            return False
