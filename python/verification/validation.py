# -*- coding: utf-8 -*-
from .validation_param import *
from .verification_code import VerificationCode

"""
    用途：数据校验
    内容：校验逻辑
    :param check_params:            检查数据的限制
    :param real_request_params:     前端请求的数据
    :return:                        参数的类对象
"""


class Validation(object):

    def __init__(self, obj, real_request_params):
        self.obj = obj                                  # 参数类
        self.check_params = self.obj.param              # 参数校验内容
        self.real_request_params = real_request_params  # 前端请求的参数
        self.req = self.obj.__dict__                    # 返回的参数对象
        self.status = True                              # 校验过程状态码
        self.error_code = None                          # 返回前端错误码
        self.error_param = None                         # 当前参数
        self.is_continue = None                         # 跳过当前参数检测信号

    def check(self):
        # 判断请求参数是否合法（请求参数名有误）
        for k in self.real_request_params.keys():
            if k not in self.check_params.keys():
                self.error_param = k
                self.error_code = VerificationCode.PARAM_ERROR.value
                self.status = False
        if self.status:
            # 取出所有需要校验参数的 "参数名" 和 "验证内容"
            for k, v in self.check_params.items():
                # 取出前端参数内容
                real_params = self.real_request_params.get(k)
                # 判断数据是否必要
                if REQUIRE in v.keys():
                    real_params = self.__v_require_params(v, real_params)
                    # 必要性判断存在错误则返回
                    if not self.status:
                        self.error_param = k
                        self.error_code = VerificationCode.REQUIRE_ERROR.value
                        break
                    # 跳过当前参数检测
                    if self.is_continue:
                        self.is_continue = None     # 重置状态
                        continue
                # 判断数据类型是否一致
                self.__v_type(k, v, real_params)
                if not self.status:
                    break
                # 数据验证完毕 更新已校验数据
                self.req[k] = real_params
        return self.status, self.error_code, self.error_param, self.obj

    # 参数必要判断
    def __v_require_params(self, v, real_params):
        is_default = None
        # 获取数据是否必要的属性
        is_require = v[REQUIRE]
        # 判断数据是否有默认值
        if DEFAULT in v.keys():
            is_default = True
        # 数据非必要|没有数据|没有默认值|数据类型不是bool，直接跳过 k 这个参数的校验
        if not is_require and not real_params and not is_default and type(real_params) != bool:
            # 激活信号 跳过当前参数的检验
            self.is_continue = True
        # 数据必要|没有数据|没有默认值|数据类型不是bool，回错误码
        elif is_require and not real_params and not is_default and type(real_params) != bool:
            # 返回错误
            self.status = False
        # 没有数据|有默认值|数据类型不是bool， 获取默认值
        elif not real_params and is_default and type(real_params) != bool:
            # 获取数据
            real_params = v[DEFAULT]
        return real_params

    # 类型判断
    def __v_type_params(self, v_type, data):
        if v_type == float and data == 0:
            data = float(data)
        if v_type == float:
            if isinstance(data, int):
                data = float(data)
        # 判断数据是否符规定
        self.status = isinstance(data, v_type)

    # 最大长度判断
    def __v_max_length_params(self, v_max_length, data):
        # 数据为必须 且 没有数据 返回错误
        if len(data) > v_max_length:
            self.status = False
        else:
            self.status = True

    # 最小长度判断
    def __v_min_length_params(self, v_min_length, data):
        if len(data) < v_min_length:
            self.status = False
        else:
            self.status = True

    # 最大长度判断
    def __v_max_params(self, max_int, data):
        # 数据为必须 且 没有数据 返回错误
        if data > max_int:
            self.status = False
        else:
            self.status = True

    # 整型最小长度判断
    def __v_min_params(self, min_int, data):
        # 数据为必须 且 没有数据 返回错误
        if data < min_int:
            self.status = False
        else:
            self.status = True

    # 判断类型 以及对应类型下的限制条件
    def __v_type(self, k, v, real_params):
        if TYPE in v.keys():
            # 0 == 0.0
            if v[TYPE] == float and real_params == 0:
                real_params = float(real_params)
            self.__v_type_params(v[TYPE], real_params)
            # 数据类型不一致，返回错误码
            if not self.status:
                self.error_param = k
                self.error_code = VerificationCode.TYPE_ERROR.value
                return
            # 数据类型为 str 或 list 需要判断长度
            if v[TYPE] == str or v[TYPE] == list:
                # 判断数据长度是否越界（最大）
                if MAXLENGTH in v.keys():
                    self.__v_max_length_params(v[MAXLENGTH], real_params)
                    if not self.status:
                        self.error_param = k
                        self.error_code = VerificationCode.MAX_LENGTH_ERROR.value
                        return
                # 判断数据长度是否越界（最小）
                if MINLENGTH in v.keys():
                    self.__v_min_length_params(v[MINLENGTH], real_params)
                    if not self.status:
                        self.error_param = k
                        self.error_code = VerificationCode.MIN_LENGTH_ERROR.value
                        return
            # 数据类型为 int 需要判断大小
            elif v[TYPE] == int or v[TYPE] == float:
                # 判断数据是否越界（最大）
                if MAX in v.keys():
                    self.__v_max_params(v[MAX], real_params)
                    if not self.status:
                        self.error_param = k
                        self.error_code = VerificationCode.MAX_ERROR.value
                        return
                # 判断数据是否越界（最小）
                if MIN in v.keys():
                    self.__v_min_params(v[MIN], real_params)
                    if not self.status:
                        self.error_param = k
                        self.error_code = VerificationCode.MIN_ERROR.value
                        return
            # 数据类型为 list 需要判断内容
            elif v[TYPE] == list:
                # 判断list下的参数是否符合标准
                for param in real_params:
                    # 如果list下的参数类型是dict 需要判断校验list的参数
                    if v[LIST_TYPE] == dict:
                        # 遍历数据下的所有数据
                        valid = Validation(v[PARAM], real_params)
                        self.status, self.error_code, self.error_param, real_params = valid.check()
                    else:
                        self.__v_type_params(v[LIST_TYPE], param)
                    if not self.status:
                        break
            # 数据类型为 dict 需要迭代判断
            elif v[TYPE] == dict:
                # 遍历数据下的所有数据
                valid = Validation(v[PARAM], real_params)
                self.status, self.error_code, self.error_param, real_params = valid.check()


