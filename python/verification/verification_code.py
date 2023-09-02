# -*- coding: utf-8 -*-
from enum import Enum
"""
    用途：数据校验
    内容：返回前端错误信息
"""


class VerificationCode(Enum):
    GET_ERROR = {'code': 1000, 'message_cn': 'GET请求格式错误', 'message_en': ''}
    JSON_ERROR = {'code': 1001, 'message_cn': 'JSON解析错误', 'message_en': ''}
    PARAM_ERROR = {'code': 1002, 'message_cn': '请求参数不合法', 'message_en': ''}
    REQUIRE_ERROR = {'code': 1003, 'message_cn': '参数为必须，不允许为空', 'message_en': ''}
    TYPE_ERROR = {'code': 1004, 'message_cn': '参数类型不合法', 'message_en': ''}
    MAX_LENGTH_ERROR = {'code': 1005, 'message_cn': '参数超过最大长度限制', 'message_en': ''}
    MIN_LENGTH_ERROR = {'code': 1006, 'message_cn': '参数超过最小长度限制', 'message_en': ''}
    MAX_ERROR = {'code': 1007, 'message_cn': '参数超过最大限制', 'message_en': ''}
    MIN_ERROR = {'code': 1008, 'message_cn': '参数超过最小限制', 'message_en': ''}

