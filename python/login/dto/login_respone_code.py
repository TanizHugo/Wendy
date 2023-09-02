# -*- coding: utf-8 -*-
from enum import Enum


class LoginResultCode(Enum):
    SUCCESS = {'code': 200, 'message_cn': '操作成功', 'message_en': ''}
    ERR = {'code': 501, 'message_cn': '操作失败', 'message_en': ''}
    PWD_ERR = {'code': 501, 'message_cn': '密码错误', 'message_en': ''}
    APPROVAL_ERR = {'code': 501, 'message_cn': '商家未通过审核', 'message_en': ''}
    SEND_CODE_ERR = {'code': 501, 'message_cn': '发送验证码失败', 'message_en': ''}
    VER_CODE_ERR = {'code': 502, 'message_cn': '验证失败', 'message_en': ''}
    VER_CODE_EXPIRED = {'code': 503, 'message_cn': '验证码过期', 'message_en': ''}
    PASSWORD_ERR = {'code': 504, 'message_cn': '密码错误', 'message_en': ''}
    LOGIN_ERR = {'code': 505, 'message_cn': '登录失败', 'message_en': ''}
    USER_NOT_EXIST = {'code': 506, 'message_cn': '账号不存在', 'message_en': ''}
    VX_40029 = {'code': 507, 'message_cn': 'code 无效', 'message_en': ''}
    VX_45011 = {'code': 508, 'message_cn': 'API 调用太频繁，请稍候再试', 'message_en': ''}
    VX_40226 = {'code': 509, 'message_cn': '高风险等级用户，小程序登录拦截 。风险等级详见用户安全解方案', 'message_en': ''}
    VX_1 = {'code': 510, 'message_cn': '系统繁忙，此时请开发者稍候再试', 'message_en': ''}
    VX_40163 = {'code': 511, 'message_cn': 'code 已经被使用', 'message_en': ''}


class OnlineResultCode(Enum):
    SUCCESS = {'code': 200, 'message_cn': '操作成功', 'message_en': ''}
    ERR = {'code': 501, 'message_cn': '操作成功', 'message_en': ''}
