# -*- coding: utf-8 -*-
import uuid
import random

"""生成随机编号"""


# 创建具有固定字段的随机编号
def create_fixed_number(length, genre):

    if genre == 'number':
        code = ''
        while len(code) != length:
            code += str(random.randint(0, 10))
    elif genre == 'character':
        code = uuid.uuid4().hex[:length]
    else:
        code = None
    return code





