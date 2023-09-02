# -*- coding: utf-8 -*-
from verification.validation_param import *                   # 限制名
from utils.data_limit import max_length, password_max_length  # 限制内容


class Add(object):

    def __init__(self):
        self.aid = None
        self.contract = None
        self.source = None
        self.illustrate = None
        self.principal = None

    param = {
        "aid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "contract": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "source": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "illustrate": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "principal": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
    }


class Inquire(object):

    def __init__(self):
        self.aid = None
        self.page = None
        self.page_size = None

    param = {
        "aid": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "page": {REQUIRE: False, TYPE: str, DEFAULT: '1'},
        "page_size": {REQUIRE: False, TYPE: str, DEFAULT: '10'},
    }


class Delete(object):

    def __init__(self):
        self.aid_list = None

    param = {
        "aid_list": {REQUIRE: True, TYPE: list, LIST_TYPE: str},
    }


class Update(object):

    def __init__(self):
        self.aid = None
        self.contract = None
        self.source = None
        self.illustrate = None
        self.principal = None

    param = {
        "aid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "contract": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "source": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "illustrate": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "principal": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
    }




