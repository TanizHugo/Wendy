# -*- coding: utf-8 -*-
from verification.validation_param import *                   # 限制名
from utils.data_limit import max_length, password_max_length  # 限制内容


class Login(object):

    def __init__(self):
        self.name = None
        self.password = None

    param = {
        "name": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "password": {REQUIRE: True, TYPE: str, MAXLENGTH: password_max_length},
    }


class VXLogin(object):

    def __init__(self):
        self.login_code = None

    param = {
        "login_code": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }


class DecodeToken(object):

    def __init__(self):
        self.token = None

    param = {
        "token": {REQUIRE: True, TYPE: str},
    }

