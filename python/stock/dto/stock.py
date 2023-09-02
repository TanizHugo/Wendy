# -*- coding: utf-8 -*-
from verification.validation_param import *             # 限制名
from utils.data_limit import max_length                 # 限制内容


class Add(object):

    def __init__(self):
        self.mid = None
        self.sid = None
        self.label_name = None
        self.stock_name = None
        self.price = None
        self.num = None
        self.type = None
        self.flowers = None
        self.material = None
        self.package = None
        self.lof = None

    param = {
        "mid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "sid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "label_name": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "stock_name": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "price": {REQUIRE: True, TYPE: float},
        "num": {REQUIRE: True, TYPE: int},
        "type": {REQUIRE: True, TYPE: int},
        "flowers": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "material": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "package": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "lof": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }


class Inquire(object):

    def __init__(self):
        self.mid = None
        self.sid = None
        self.label_name = None
        self.stock_name = None
        self.name = None
        self.type = None
        self.page = None
        self.page_size = None

    param = {
        "mid": {REQUIRE: False, TYPE: str},
        "sid": {REQUIRE: False, TYPE: str},
        "label_name": {REQUIRE: False, TYPE: str},
        "stock_name": {REQUIRE: False, TYPE: str},
        "name": {REQUIRE: False, TYPE: str},
        "type": {REQUIRE: False, TYPE: str},
        "page": {REQUIRE: False, TYPE: str, DEFAULT: '1'},
        "page_size": {REQUIRE: False, TYPE: str, DEFAULT: '10'},
    }


class Delete(object):

    def __init__(self):
        self.sid = None

    param = {
        "sid": {REQUIRE: True, TYPE: str},
    }


class Update(object):

    def __init__(self):
        self.mid = None
        self.sid = None
        self.label_name = None
        self.stock_name = None
        self.price = None
        self.num = None
        self.type = None
        self.flowers = None
        self.material = None
        self.package = None
        self.lof = None

    param = {
        "mid": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "sid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "label_name": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "stock_name": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "price": {REQUIRE: False, TYPE: float},
        "num": {REQUIRE: False, TYPE: int},
        "type": {REQUIRE: False, TYPE: int},
        "flowers": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "material": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "package": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "lof": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
    }





