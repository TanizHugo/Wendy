# -*- coding: utf-8 -*-

from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from order.models import Order, OrderStock
from cart.models import Stock, CartStock, ShopCart
from stock.models import MerchantStock
from order.dto.order_respone_code import OrderResultCode
from utils.model_control import ModelControl
from utils.generate_uuid import create_fixed_number
from order.config.order_state import *


class OrderService(object):

    # 新增订单（购买）
    def add(self, data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        # 写入数据库
        try:
            with transaction.atomic():
                self.models_control(data_obj)            # 创建用户组表（数据库）
                res_code = OrderResultCode.SUCCESS.value         # 成功
        except:
            res_code = OrderResultCode.ADD_ERR.value        # 注册失败

        return res_code, res_data

    # 订单查询
    def inquire(self, data_obj):
        res_code = None                     # http 返回码
        res_data = dict()                   # http 返回数据
        order = Order.objects.all()  # 查询所有数据

        # 数据存在？
        if not order:
            res_code = OrderResultCode.SUCCESS.value             # 成功
            return res_code, res_data
        try:
            data, res_data['total'] = self.inquire_obj(data_obj)        # 复杂查询
            res_data['data'] = self.data_tidy(data)
            res_code = OrderResultCode.SUCCESS.value             # 成功
        except:
            res_code = OrderResultCode.INQUIRE_ERR.value             # 查询失败

        return res_code, res_data

    # 订单修改
    def update(self, data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据
        try:
            Order.objects.get(oid=data_obj.oid)
        except:
            res_code = OrderResultCode.NOT_EXIST.value
            return res_code, res_data

        try:
            with transaction.atomic():
                self.update_model(data_obj)
                res_code = OrderResultCode.SUCCESS.value
        except:
            res_code = OrderResultCode.UPDATE_ERR.value

        return res_code, res_data

    # 订单ID生成
    @staticmethod
    def create_oid():
        oid = create_fixed_number(32, 'character')
        return oid

    # 整理数据（返回）
    @staticmethod
    def data_tidy(orders):
        res_data = list()
        for data in orders:
            order_stock = OrderStock.objects.filter(order=data)
            for obj in order_stock:
                stock = obj.stock
                merchant = MerchantStock.objects.get(stock=stock).merchant
                order_info = {
                    'oid': data.oid,
                    'openid': data.openid,
                    'state': data.state,
                    'finish_time': data.finish_time,
                    'book_time': data.book_time,
                    'user_name': data.user_name,
                    'phone': data.phone,
                    'way': data.way,
                    'create_time': data.create_time,
                    'quantity': obj.quantity,
                    'pay': obj.pay,
                }
                stock_info = {
                    'sid': stock.sid,
                    'stock_name': stock.stock_name,
                    'price': stock.price,
                }
                merchant_info = {
                    'mid': merchant.mid,
                    'name': merchant.name,
                    'address': merchant.address,
                }
                res_data.append({
                    'order_info': order_info,
                    'stock_info': stock_info,
                    'merchant_info': merchant_info,
                })
        return res_data

    # 复杂查询
    @staticmethod
    def inquire_obj(data_obj):
        order_obj = list()

        # 分页查询
        page = int(data_obj.page)
        page_size = int(data_obj.page_size)
        start = (page - 1) * page_size
        end = page_size * page

        # 精准查询
        if data_obj.oid or data_obj.state or data_obj.openid:
            q = Q()
            q.connector = 'AND'
            if data_obj.oid:
                q.children.append(('oid', data_obj.oid))
            elif data_obj.state:
                q.children.append(('state', int(data_obj.state)))
            elif data_obj.openid:
                q.children.append(('openid', data_obj.openid))
            order_obj.append(set(Order.objects.filter(q)))

        # 商家外键查询
        if data_obj.mid:
            data_list = list()
            q = Q()
            order_stock = OrderStock.objects.all()
            for obj in order_stock:
                merchant = MerchantStock.objects.get(stock=obj.stock).merchant
                if merchant.mid == data_obj.mid:
                    data_list.append(obj.order)

            order_obj.append(set(data_list))

        # 商品标外键查询
        if data_obj.sid:
            data_list = list()
            order_stock = OrderStock.objects.filter(sid=data_obj.sid)
            for obj in order_stock:
                if obj.stock.sid == data_obj.sid:
                    data_list.append(obj.order)
            order_obj.append(set(data_list))

        # 所有内容
        order_obj.append(set(Order.objects.all()))

        orders = list(set.intersection(*[order for order in order_obj]))    # 通过元组 找出同类项

        return orders[start:end], len(orders)

    # 数据表
    def add_model(self, data_obj):
        data_obj.state = NOORDER                    # 订单的状态（未接单）

        # 增加订单信息表
        dict_param = ModelControl.copy_model(Order, data_obj)
        order = Order(**dict_param)
        order.save()

        # 增加订单购物内容表
        data_obj.order = order
        dict_param = ModelControl.copy_model(OrderStock, data_obj)
        order_stock = OrderStock(**dict_param)
        order_stock.save()

    # 数据表添加
    def models_control(self, data_obj):
        # 购物车生成订单
        if data_obj.cart:
            carts = CartStock.objects.filter(shop_cart_id=data_obj.openid)
            mid_oid = dict()
            for cart in carts:
                if cart.select_state:
                    data_obj.stock = cart.stock
                    data_obj.quantity = cart.quantity
                    data_obj.pay = cart.shop_cart.select_money
                    merchant = MerchantStock.objects.get(stock=cart.stock).merchant

                    # 以商家为形式进行封装 写入数据库
                    if merchant not in mid_oid.keys():
                        oid = self.create_oid()  # 生成oid
                        mid_oid[merchant] = oid
                        data_obj.oid = oid
                    else:
                        data_obj.oid = mid_oid[merchant]

                    self.add_model(data_obj)        # 添加数据库（订单）

                    cart.delete()                   # 提交后从购物车移出

                else:
                    continue
        # 直接购买
        else:
            stock = Stock.objects.get(sid=data_obj.sid)
            _price = stock.price
            data_obj.stock = stock
            data_obj.oid = self.create_oid()        # 生成oid
            data_obj.pay = round(_price * data_obj.quantity)
            self.add_model(data_obj)

    # 数据表修改
    @staticmethod
    def update_model(data_obj):
        # 用户表的添加
        order = Order.objects.filter(oid=data_obj.oid)
        dict_param = ModelControl.copy_model(Order, data_obj)        # 获取写入表的数据
        order.update(**dict_param)                                   # 修改&写入

        # 已签收
        if data_obj.state == SING:
            order_stock = OrderStock.objects.filter(order_id=data_obj.oid)
            for data in order_stock:
                stock = Stock.objects.get(sid=data.stock.sid)

                if data_obj.openid:
                    # 购物车（支付状态）
                    try:
                        shop_cart = ShopCart.objects.get(openid=data_obj.openid)
                        cart_stock = CartStock.objects.get(shop_cart=shop_cart, stock=stock)
                        cart_stock.paid = True
                        cart_stock.save()
                    except:
                        pass

                # 商品销量
                try:
                    stock.sold += 1
                    stock.num -= 1
                    stock.save()
                except:
                    pass

