# -*- coding: utf-8 -*-
import copy


class ModelControl(object):

    @staticmethod
    def copy_model(model_obj, data_obj):
        data = data_obj.__dict__                                # dict取出所有参数
        dict_param = dict()                                     # 返回一条数据
        obj = model_obj._meta.fields                            # 获取数据表所有的参数

        # 取出每一列的列名
        for i in range(len(obj)):
            param = data.get(obj[i].name)                       # 根据参数名取出数据值
            if param:
                dict_param[obj[i].name] = copy.deepcopy(param)  # 深拷贝数据
        return dict_param

