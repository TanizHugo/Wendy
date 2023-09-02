# -*- coding: utf-8 -*-
from verification.validation_param import *                   # 限制名
from utils.data_limit import max_length, password_max_length  # 限制内容


class Add(object):

    def __init__(self):
        self.code = None
        self.limit_time = None

    param = {
        "code": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "limit_time": {REQUIRE: True, TYPE: int},
    }


class Inquire(object):

    def __init__(self):
        self.code = None
        self.license_state = None
        self.page = None
        self.page_size = None

    param = {
        "code": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "license_state": {REQUIRE: False, TYPE: str},
        "page": {REQUIRE: False, TYPE: str, DEFAULT: '1'},
        "page_size": {REQUIRE: False, TYPE: str, DEFAULT: '10'},
    }


class Delete(object):

    def __init__(self):
        self.code = None

    param = {
        "code": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }


class Update(object):

    def __init__(self):
        self.code = None
        self.license_state = None
        self.limit_time = None

    param = {
        "code": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "license_state": {REQUIRE: False, TYPE: int},
        "limit_time": {REQUIRE: False, TYPE: int},
    }
