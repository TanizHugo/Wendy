# -*- coding: utf-8 -*-
from verification.validation_param import *     # 限制名
from utils.data_limit import max_length         # 限制内容


class Add(object):

    def __init__(self):
        self.mid = None
        self.label_name = None

    param = {
        "mid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "label_name": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }


class Inquire(object):

    def __init__(self):
        self.mid = None

    param = {
        "mid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }


class Delete(object):

    def __init__(self):
        self.mid = None
        self.label_name = None

    param = {
        "mid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "label_name": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }
