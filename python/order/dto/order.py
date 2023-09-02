# -*- coding: utf-8 -*-
from verification.validation_param import *                   # 限制名
from utils.data_limit import max_length                       # 限制内容


class Add(object):

    def __init__(self):
        self.cart = None
        self.sid = None
        self.book_time = None
        self.openid = None
        self.user_name = None
        self.phone = None
        self.quantity = None
        self.way = None

    param = {
        "cart": {REQUIRE: True, TYPE: bool},
        "sid": {REQUIRE: False, TYPE: str},
        "book_time": {REQUIRE: True, TYPE: int},
        "openid": {REQUIRE: True, TYPE: str},
        "user_name": {REQUIRE: True, TYPE: str},
        "phone": {REQUIRE: True, TYPE: str},
        "way": {REQUIRE: True, TYPE: str},
        "quantity": {REQUIRE: False, TYPE: int},
    }


class Update(object):

    def __init__(self):
        self.oid = None
        self.openid = None
        self.book_time = None
        self.state = None

    param = {
        "openid": {REQUIRE: False, TYPE: str},
        "oid": {REQUIRE: True, TYPE: str, MAXLENGTH: max_length},
        "book_time": {REQUIRE: False, TYPE: int},
        "state": {REQUIRE: False, TYPE: int},
    }


class Inquire(object):

    def __init__(self):
        self.oid = None
        self.sid = None
        self.mid = None
        self.openid = None
        self.state = None
        self.page = None
        self.page_size = None

    param = {
        "oid": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "sid": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "mid": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "openid": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "state": {REQUIRE: False, TYPE: str, MAXLENGTH: max_length},
        "page": {REQUIRE: False, TYPE: str, DEFAULT: '1'},
        "page_size": {REQUIRE: False, TYPE: str, DEFAULT: '10'},
    }

