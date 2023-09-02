# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
from wendy.settings import LANGUAGE

"""
    用途：数据校验
    内容：返回的结果的封装
"""


class Response(object):

    def response_json(self, res_code, res_data):
        # 没有返回内容 设置为默认内容
        if res_code is None:
            res_code = dict()
            res_code['code'] = 0
            res_code['message_cn'] = '返回错误'
        # 没有data 则不需要返回data
        if res_data is None:

            return JsonResponse({
                'code': res_code['code'],
                'message': self.decide_language(res_code),
            }, )
        else:
            return JsonResponse({
                'code': res_code['code'],
                'message': self.decide_language(res_code),
                'data': res_data,
            })

    # 中英文
    @staticmethod
    def decide_language(res_code):
        if LANGUAGE == 'cn':
            return res_code['message_cn']
        elif LANGUAGE == 'en':
            return res_code['message_en']

    @staticmethod
    def response_file(file_obj):
        with open(file_obj.file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=file_obj.content_type, charset='utf-8')

            # 设置为attachment,浏览器则直接进行下载，纵使他能够预览该类型的文件
            # response['Content-Disposition'] = "attachment; filename={0}".format(file_obj.file_name).encode('utf-8',
            #                                                                                                'ISO-8859-1')

            # 设置为inline,如果浏览器支持该文件类型的预览，就会打开，而不是下载
            response['Content-Disposition'] = "inline; filename={0}".format(file_obj.file_name).encode('utf-8',
                                                                                                       'ISO-8859-1')
            response['Access-Control-Allow-Origin'] = '*'
            response['Server'] = '*'

        return response

