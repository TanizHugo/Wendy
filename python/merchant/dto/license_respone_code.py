# -*- coding: utf-8 -*-
from enum import Enum


class LicenseResultCode(Enum):
    SUCCESS = {'code': 200, 'message_cn': '操作成功', 'message_en': ''}
    CREATE_CODE_ERR = {'code': 501, 'message_cn': '许可码生成失败', 'message_en': ''}
    ADD_ERR = {'code': 502, 'message_cn': '添加失败', 'message_en': ''}
    UPDATE_ERR = {'code': 502, 'message_cn': '修改失败', 'message_en': ''}
    INQUIRE_ERR = {'code': 503, 'message_cn': '查询失败', 'message_en': ''}
    NAME_EXIST = {'code': 506, 'message_cn': '许可码已经存在', 'message_en': ''}
    NAME_NOT_EXIST = {'code': 506, 'message_cn': '许可码不存在', 'message_en': ''}
    DELETE_ERR = {'code': 508, 'message_cn': '删除失败', 'message_en': ''}
