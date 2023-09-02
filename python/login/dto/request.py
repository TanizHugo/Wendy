# -*- coding: utf-8 -*-
from verification.validation_param import *                 # 限制名
from utils.data_limit import max_length                     # 限制内容


class DeleteOnlineUser(object):

    def __init__(self):
        self.openid = None

    param = {
        "openid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }


