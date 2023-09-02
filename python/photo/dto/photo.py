# -*- coding: utf-8 -*-
from verification.validation_param import *                   # 限制名
from utils.data_limit import max_length                         # 限制内容


class Inquire(object):

    def __init__(self):
        self.id = None
        self.type = None

    param = {
        "id": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "type": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }


class Delete(object):

    def __init__(self):
        self.id = None

    param = {
        "id": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }



