# -*- coding: utf-8 -*-
from enum import Enum


class CartResultCode(Enum):
    SUCCESS = {'code': 200, 'message_cn': '操作成功', 'message_en': ''}
    STOCK_EXIST = {'code': 604, 'message_cn': '商品存在购物车', 'message_en': ''}
    ADD_ERR = {'code': 605, 'message_cn': '添加失败', 'message_en': ''}
    UPDATE_ERR = {'code': 602, 'message_cn': '修改失败', 'message_en': ''}
    OUT_RANGE = {'code': 605, 'message_cn': '超出范围', 'message_en': ''}
    INQUIRE_ERR = {'code': 603, 'message_cn': '查询失败', 'message_en': ''}
    DELETE_ERR = {'code': 607, 'message_cn': '删除失败', 'message_en': ''}

