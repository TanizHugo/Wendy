# -*- coding: utf-8 -*-
import time
import json

from wendy.settings import cache
from login.models import RequestAdvertise, RequestUser
from login.dto.login_respone_code import OnlineResultCode


class RequestService(object):

    # 获取在线人数
    @staticmethod
    def get_online_num():
        res_code = None
        res_data = None

        usage = UsageStatus()

        try:
            num = usage.get_cache_user()
            res_data = {'num_online': num}
            res_code = OnlineResultCode.SUCCESS.value           # 成功
        except:
            res_code = OnlineResultCode.ERR.value               # 失败

        return res_code, res_data

    # 用户登出
    @staticmethod
    def del_online_user(data_obj):
        res_code = None
        res_data = None

        usage = UsageStatus()

        if usage.del_cache_user(data_obj.openid):
            res_code = OnlineResultCode.SUCCESS.value           # 成功
        else:
            res_code = OnlineResultCode.ERR.value               # 失败

        return res_code, res_data

    # 访问人存储数据表
    @staticmethod
    def add_user_db(openid):
        user = RequestUser(
            openid=openid,
            req_time=int(time.time())
        )
        user.save()

    # 广告点击存数据表
    @staticmethod
    def add_ad_db(openid, req):
        params = json.loads(req.body)
        aid = params.get('aid', None)
        ad = RequestAdvertise(
            openid=openid,
            req_time=int(time.time()),
            aid=aid,
        )
        ad.save()


# 在线人数
class UsageStatus(object):

    def __init__(self):
        self.user_state = cache.get(key='usage')
        if self.user_state is None:
            self.user_state = list()

    # 刷新用户在线状态
    def refresh(self, user_name):
        _user_state = self.user_state.copy()
        # 户是不在记录内
        if user_name not in _user_state:
            _user_state.append(user_name)
        cache.set(key='usage', value=_user_state)

    # 获取所有缓存内的用户状态
    def get_cache_user(self):
        _user_state = self.user_state.copy()
        return len(_user_state)

    # 将用户从缓存中剔除
    def del_cache_user(self, user_name):
        _user_state = self.user_state.copy()
        if not _user_state or user_name not in _user_state:
            state = False
        else:
            _user_state.pop(user_name)
            cache.set(key='usage', value=_user_state)
            state = True
        return state

