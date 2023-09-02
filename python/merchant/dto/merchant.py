# -*- coding: utf-8 -*-
from verification.validation_param import *                   # 限制名
from utils.data_limit import max_length, password_max_length  # 限制内容


class Add(object):

    def __init__(self):
        self.mid = None
        self.user_name = None
        self.phone = None
        self.password = None
        self.address = None
        self.uid = None
        self.name = None
        self.code = None

    param = {
        "mid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "name": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "phone": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "password": {REQUIRE: True, TYPE: str, MAXLENGTH: password_max_length},
        "address": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "uid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "user_name": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "code": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }


class Inquire(object):

    def __init__(self):
        self.approval = None
        self.mid = None
        self.name = None
        self.code = None
        self.license_state = None
        self.page = None
        self.page_size = None

    param = {
        "approval": {REQUIRE: False, TYPE: str},
        "mid": {REQUIRE: False, TYPE: str},
        "name": {REQUIRE: False, TYPE: str},
        "license_state": {REQUIRE: False, TYPE: str},
        "code": {REQUIRE: False, TYPE: str},
        "page": {REQUIRE: False, TYPE: str, DEFAULT: '1'},
        "page_size": {REQUIRE: False, TYPE: str, DEFAULT: '10'},
    }


class Delete(object):

    def __init__(self):
        self.mid = None

    param = {
        "mid": {REQUIRE: True, TYPE: str},
    }


class Update(object):

    def __init__(self):
        self.mid = None
        self.name = None
        self.address = None

    param = {
        "mid": {REQUIRE: True, TYPE: str},
        "name": {REQUIRE: False, TYPE: str},
        "address": {REQUIRE: False, TYPE: str},
    }


class Pass(object):

    def __init__(self):
        self.code = None

    param = {
        "code": {REQUIRE: True, TYPE: str},
    }


class Reject(object):

    def __init__(self):
        self.code = None
        self.reason = None

    param = {
        "code": {REQUIRE: True, TYPE: str},
        "reason": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }


