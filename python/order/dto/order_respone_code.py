# -*- coding: utf-8 -*-
from enum import Enum


class OrderResultCode(Enum):
    SUCCESS = {'code': 200, 'message_cn': '操作成功', 'message_en': ''}
    CREATE_UUID_ERR = {'code': 601, 'message_cn': '编号生成失败', 'message_en': ''}
    UPDATE_ERR = {'code': 602, 'message_cn': '修改失败', 'message_en': ''}
    INQUIRE_ERR = {'code': 603, 'message_cn': '查询失败', 'message_en': ''}
    ID_EXIST = {'code': 604, 'message_cn': '店铺名已经存在', 'message_en': ''}
    ADD_ERR = {'code': 605, 'message_cn': '添加失败', 'message_en': ''}
    DELETE_ERR = {'code': 607, 'message_cn': '删除失败', 'message_en': ''}
    LABEL_NAME_EXIST = {'code': 608, 'message_cn': '·   ', 'message_en': ''}
    NOT_EXIST = {'code': 604, 'message_cn': '订单不存在', 'message_en': ''}

