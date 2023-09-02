# -*- coding: utf-8 -*-
from verification.validation_param import *                   # 限制名
from utils.data_limit import max_length                       # 限制内容


class Add(object):

    def __init__(self):
        self.openid = None
        self.sid = None
        self.quantity = None

    param = {
        "openid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "sid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "quantity": {REQUIRE: True, TYPE: int},
    }


class Delete(object):

    def __init__(self):
        self.openid = None
        self.sid_list = None

    param = {
        "openid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "sid_list": {REQUIRE: True, TYPE: list, LIST_TYPE: str},
    }


class Inquire(object):

    def __init__(self):
        self.openid = None

    param = {
        "openid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }


class UpdateCartNum(object):

    def __init__(self):
        self.openid = None
        self.sid = None
        self.iod = None

    param = {
        "openid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "sid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "iod": {REQUIRE: True, TYPE: bool},
    }


class UpdateCartAllState(object):

    def __init__(self):
        self.openid = None

    param = {
        "openid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }


class UpdateCartStockState(object):

    def __init__(self):
        self.openid = None
        self.sid_list = None

    param = {
        "openid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "sid_list": {REQUIRE: True, TYPE: list, LIST_TYPE: str},
    }

