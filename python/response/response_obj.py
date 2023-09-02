# -*- coding: utf-8 -*-


class ResponseFile(object):

    def __init__(self):
        self.file_path = None       # 文件路径用于打开文件
        self.content_type = None    # 媒体类型
        self.file_name = None       # 文件名
