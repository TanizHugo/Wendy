# -*- coding: utf-8 -*-
from enum import Enum


class PhotoResultCode(Enum):
    SUCCESS = {'code': 200, 'message_cn': '操作成功', 'message_en': ''}
    EXIST = {'code': 501, 'message_cn': 'id重复', 'message_en': ''}
    NOT_EXIST = {'code': 502, 'message_cn': '图片不存在', 'message_en': ''}
    UPLOAD_ERR = {'code': 501, 'message_cn': '图片上传失败', 'message_en': ''}
    INQUIRE_ERR = {'code': 502, 'message_cn': '图片获取失败', 'message_en': ''}
    DELETE_ERR = {'code': 503, 'message_cn': '图片删除失败', 'message_en': ''}



