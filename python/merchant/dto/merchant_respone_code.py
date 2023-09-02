# -*- coding: utf-8 -*-
from enum import Enum


class MerchantResultCode(Enum):
    SUCCESS = {'code': 200, 'message_cn': '操作成功', 'message_en': ''}
    CREATE_UUID_ERR = {'code': 501, 'message_cn': '编号生成失败', 'message_en': ''}
    NOT_EXIST = {'code': 502, 'message_cn': '店铺不存在', 'message_en': ''}
    UPDATE_ERR = {'code': 502, 'message_cn': '修改失败', 'message_en': ''}
    INQUIRE_ERR = {'code': 503, 'message_cn': '查询失败', 'message_en': ''}
    PASS_ERR = {'code': 504, 'message_cn': '通过失败', 'message_en': ''}
    REJECT_ERR = {'code': 505, 'message_cn': '驳回失败', 'message_en': ''}
    NAME_EXIST = {'code': 506, 'message_cn': '店铺名已经存在', 'message_en': ''}
    CODE_REE = {'code': 506, 'message_cn': '许可码错误', 'message_en': ''}
    REGISTER_ERR = {'code': 507, 'message_cn': '注册失败', 'message_en': ''}
    DELETE_ERR = {'code': 508, 'message_cn': '删除失败', 'message_en': ''}
