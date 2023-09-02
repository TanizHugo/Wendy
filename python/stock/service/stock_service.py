# -*- coding: utf-8 -*-

from django.db import transaction
from django.db.models import Q

from stock.models import Stock, MerchantStock, Merchant, StockLabel, Label
from stock.dto.stok_respone_code import StockResultCode
from utils.model_control import ModelControl
from utils.generate_uuid import create_fixed_number


class StockService(object):

    # 商品添加
    def stock_add(self, data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        # 商鋪名重复检查
        try:
            Stock.objects.get(stock_name=data_obj.stock_name)
            res_code = StockResultCode.NAME_EXIST.value      # 商品名已经存在
            return res_code, res_data
        except:
            pass

        # 写入数据库
        try:
            with transaction.atomic():
                self.add_model(data_obj)            # 创建用户组表（数据库）
                res_code = StockResultCode.SUCCESS.value         # 成功
        except:
            res_code = StockResultCode.ADD_ERR.value        # 添加失败

        return res_code, res_data

    # 商品查询
    def stock_inquire(self, data_obj):
        res_code = None                     # http 返回码
        res_data = dict()                   # http 返回数据
        stocks = Stock.objects.all()        # 查询所有数据

        # 数据存在？
        if not stocks:
            res_code = StockResultCode.SUCCESS.value             # 成功
            return res_code, res_data
        try:
            data, res_data['total'] = self.inquire_obj(data_obj)        # 复杂查询
            res_data['data'] = self.data_tidy(data)
            res_code = StockResultCode.SUCCESS.value             # 成功
        except:
            res_code = StockResultCode.INQUIRE_ERR.value             # 查询失败

        return res_code, res_data

    # 商品刪除
    @staticmethod
    def stock_delete(data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        # 写入数据库
        try:
            with transaction.atomic():
                Stock.objects.get(sid=data_obj.sid).delete()
                res_code = StockResultCode.SUCCESS.value         # 成功
        except:
            res_code = StockResultCode.DELETE_ERR.value          # 删除失败
        return res_code, res_data

    # 商品修改
    def stock_update(self, data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据
        try:
            Merchant.objects.get(mid=data_obj.mid)
        except:
            res_code = StockResultCode.NOT_EXIST.value
            return res_code, res_data

        try:
            with transaction.atomic():
                self.update_model(data_obj)
                res_code = StockResultCode.SUCCESS.value
        except:
            res_code = StockResultCode.UPDATE_ERR.value
        return res_code, res_data

    # 商家ID生成
    @staticmethod
    def create_sid():
        res_code = None                     # http 返回码
        res_data = dict()                   # http 返回数据
        sid = create_fixed_number(16, 'number')
        if sid:
            res_code = StockResultCode.SUCCESS.value
            res_data['sid'] = sid
        else:
            res_code = StockResultCode.CREATE_UUID_ERR.value
        return res_code, res_data

    # 整理数据（返回）
    @staticmethod
    def data_tidy(stocks):
        res_data = list()
        for stock in stocks:
            merchant = MerchantStock.objects.get(stock=stock).merchant
            label = StockLabel.objects.get(stock=stock).label
            res_data.append({
                'sid': stock.sid,
                'stock_name': stock.stock_name,
                'price': stock.price,
                'num': stock.num,
                'sold': stock.sold,
                'type': stock.type,
                'flowers': stock.flowers,
                'material': stock.material,
                'package': stock.package,
                'lof': stock.lof,
                'mid': merchant.mid,
                'name': merchant.name,
                'address': merchant.address,
                'label_name': label.label_name,
            })
        return res_data

    # 复杂查询
    @staticmethod
    def inquire_obj(data_obj):
        stock_obj = list()

        # 分页查询
        page = int(data_obj.page)
        page_size = int(data_obj.page_size)
        start = (page - 1) * page_size
        end = page_size * page

        # 精准查询
        if data_obj.sid or data_obj.stock_name:
            q = Q()
            q.connector = 'OR'
            if data_obj.sid:
                q.children.append(('sid', data_obj.sid))
            elif data_obj.stock_name:
                q.children.append(('stock_name', data_obj.stock_name))
            stock_obj.append(set(Stock.objects.filter(q)))

        # 商家外键查询
        if data_obj.mid or data_obj.name:
            q = Q()
            q.connector = 'OR'
            if data_obj.mid:
                q.children.append(('mid', data_obj.mid))
            elif data_obj.name:
                q.children.append(('name', data_obj.name))
            merchant = Merchant.objects.filter(q)
            merchant_stocks = MerchantStock.objects.filter(merchant=merchant[0])
            stock_obj.append(set([k.stock for k in merchant_stocks]))

        # 标签外键查询
        if data_obj.label_name and data_obj.mid:
            merchant = Merchant.objects.get(mid=data_obj.mid)
            label = Label.objects.get(merchant=merchant, label_name=data_obj.label_name)
            stock_labels = StockLabel.objects.filter(label=label)
            stock_obj.append(set([k.stock for k in stock_labels]))

        # 类型查询
        if data_obj.type:
            stock_obj.append(set(Stock.objects.filter(type=data_obj.type)))

        # 所有内容
        stock_obj.append(set(Stock.objects.all()))

        stocks = list(set.intersection(*[stock for stock in stock_obj]))    # 通过元组 找出同类项

        return stocks[start:end], len(stocks)

    # 数据表添加
    @staticmethod
    def add_model(data_obj):

        # 商品数据表
        dict_param = ModelControl.copy_model(Stock, data_obj)
        stock = Stock(**dict_param)
        stock.save()

        # 商家与商品关系表
        data_obj.stock = stock
        merchant = Merchant.objects.get(mid=data_obj.mid)
        data_obj.merchant = merchant
        dict_param = ModelControl.copy_model(MerchantStock, data_obj)
        merchant_stock = MerchantStock(**dict_param)
        merchant_stock.save()

        # 商品与标签关系表
        data_obj.label = Label.objects.get(merchant=merchant, label_name=data_obj.label_name)
        dict_param = ModelControl.copy_model(StockLabel, data_obj)
        stock_label = StockLabel(**dict_param)
        stock_label.save()

    # 数据表修改
    @staticmethod
    def update_model(data_obj):
        # 商品信息修改
        stock = Stock.objects.filter(sid=data_obj.sid)
        dict_param = ModelControl.copy_model(Stock, data_obj)        # 获取写入表的数据
        stock.update(**dict_param)                                   # 修改&写入

        if data_obj.mid and data_obj.label_name:
            # 删除旧标签
            stock = Stock.objects.get(sid=data_obj.sid)
            # 标签修改
            merchant = Merchant.objects.get(mid=data_obj.mid)
            label = Label.objects.get(merchant=merchant, label_name=data_obj.label_name)
            stock_label = StockLabel.objects.get(stock=stock)
            stock_label.label = label
            stock_label.save()

