# -*- coding: utf-8 -*-
from verification.validation_param import *                 # 限制名
from utils.data_limit import max_length                     # 限制内容


class SendCode(object):

    def __init__(self):
        self.phone = None

    param = {
        "phone": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }


class VerCode(object):

    def __init__(self):
        self.phone = None
        self.code = None

    param = {
        "phone": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "code": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }

