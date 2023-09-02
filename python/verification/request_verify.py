# -*- coding: utf-8 -*-
import json
from functools import wraps

from verification.verification_code import VerificationCode
from response.response import Response
from verification.validation import Validation


def request_verify(verify_class):
    """
        用途：数据校验
        用法：在views方法上加装饰器
    """
    def decorator(func):
        @wraps(func)
        def inner(req, *args):
            obj = verify_class()            # 生成对象
            error_code = None               # http：code和message
            res_data = None                 # http：报错参数
            status = None                   # 状态值
            correct_request_params = None   # 检验后正确的参数
            real_request_params = None      # 前端参数
            response = Response()
            # 获取方法
            try:
                method = str(req.method).lower()
            except:
                req = req.request
                method = str(req.method).lower()
            # get请求传参
            if method == 'get':
                # 获取请求内容
                try:
                    real_request_params = req.GET
                    status = True
                except:
                    error_code = VerificationCode.GET_ERROR.value
                    status = False
            # method == post 的情况
            elif method == 'post' or method == 'delete' or method == 'put':
                # 判断参数格式是否合法（合法为JSON文件）
                try:
                    real_request_params = json.loads(req.body)
                    status = True
                except:
                    error_code = VerificationCode.JSON_ERROR.value
                    status = False
                # 开始参数校验部分
            if status:
                # 循环验证的参数
                valid = Validation(obj, real_request_params)
                # 获取：状态值 错误码+信息 报错的参数 数据校验后正确的参数
                status, error_code, res_data, correct_request_params = valid.check()
            # 经过参数校验后是否正确
            if not status:
                return response.response_json(error_code, res_data)
            # 返回正确的内容
            return func(*args, correct_request_params)
        return inner
    return decorator
