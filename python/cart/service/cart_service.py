# -*- coding: utf-8 -*-

from django.db import transaction
from django.db.models import Q

from cart.models import ShopCart, CartStock
from stock.models import Stock, MerchantStock
from merchant.models import Registrant, Merchant, MerchantRegistrant
from cart.dto.cart_respone_code import CartResultCode
from utils.model_control import ModelControl
from utils.generate_uuid import create_fixed_number


class CartService(object):

    # 购物车添加
    def add(self, data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        # 商品是否在购物车
        try:
            CartStock.objects.get(shop_cart_id=data_obj.openid, stock_id=data_obj.sid)
            res_code = CartResultCode.STOCK_EXIST.value        # 商品已经在购物车中
            return res_code, res_data
        except:
            pass

        # 添加数据
        try:
            with transaction.atomic():
                self.add_model(data_obj)
                res_code = CartResultCode.SUCCESS.value         # 成功
        except:
            res_code = CartResultCode.ADD_ERR.value             # 添加失败
        return res_code, res_data

    # 购物车查询
    def inquire(self, data_obj):
        res_code = None                     # http 返回码
        res_data = dict()                   # http 返回数据
        carts = ShopCart.objects.all()  # 查询所有数据

        # 数据存在？
        if not carts:
            res_code = CartResultCode.SUCCESS.value             # 成功
            return res_code, res_data
        try:
            self.refresh_cart_table(data_obj.openid)                # 刷新购物车
            data, res_data['total'] = self.inquire_obj(data_obj)        # 复杂查询
            res_data['data'] = self.data_tidy(data)
            res_code = CartResultCode.SUCCESS.value             # 成功
        except:
            res_code = CartResultCode.INQUIRE_ERR.value             # 查询失败

        return res_code, res_data

    # 购物车内容批量刪除
    @staticmethod
    def delete(data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        # 写入数据库
        try:
            with transaction.atomic():
                for sid in data_obj.sid_list:
                    CartStock.objects.get(stock_id=sid).delete()
                res_code = CartResultCode.SUCCESS.value         # 成功
        except:
            res_code = CartResultCode.DELETE_ERR.value          # 删除失败
        return res_code, res_data

    # 购物车商品选购数量修改
    def cart_stock_num_update(self, data_obj):
        res_code = None                     # http 返回码
        res_data = None                     # http 返回数据

        # 商品是否在购物车
        try:
            cart_stock = CartStock.objects.get(shop_cart_id=data_obj.openid, stock_id=data_obj.sid)
            quantity = cart_stock.quantity
            if data_obj.iod and quantity <= 255:
                cart_stock.quantity += 1
                res_code = CartResultCode.SUCCESS.value     # 成功
                cart_stock.save()
            elif not data_obj.iod and quantity > 1:
                cart_stock.quantity -= 1
                res_code = CartResultCode.SUCCESS.value     # 成功
                cart_stock.save()
            else:
                res_code = CartResultCode.OUT_RANGE.value   # 超出范围
            self.refresh_cart_table(data_obj.openid)        # 刷新购物车
        except:
            res_code = CartResultCode.STOCK_EXIST.value  # 商品已经在购物车中
        return res_code, res_data

    # 购物车全选
    def cart_all_state_update(self, data_obj):
        res_code = None                 # http 返回码
        res_data = None                 # http 返回数据

        select_all = ShopCart.objects.get(openid=data_obj.openid).select_all    # 获取全选状态
        cart_data = CartStock.objects.filter(shop_cart_id=data_obj.openid)

        # 修改购物车所有选中状态
        try:
            for obj in cart_data:
                if select_all:
                    obj.select_state = False
                else:
                    obj.select_state = True
                obj.save()
            self.refresh_cart_table(data_obj.openid)        # 刷新购物车
            res_code = CartResultCode.SUCCESS.value         # 成功
        except:
            res_code = CartResultCode.UPDATE_ERR.value      # 修改失败
        return res_code, res_data

    # 购物车内容选中
    def cart_stock_state_update(self, data_obj):
        res_code = None                 # http 返回码
        res_data = None                 # http 返回数据

        # 修改购物车选中商品选中
        try:
            for sid in data_obj.sid_list:
                cart_data = CartStock.objects.get(shop_cart_id=data_obj.openid, stock_id=sid)
                cart_data.select_state = not cart_data.select_state
                cart_data.save()
            self.refresh_cart_table(data_obj.openid)            # 刷新购物车
            res_code = CartResultCode.SUCCESS.value             # 成功
        except:
            res_code = CartResultCode.UPDATE_ERR.value          # 修改失败
        return res_code, res_data

    # 整理数据（返回）
    @staticmethod
    def data_tidy(data):
        res_data = dict()

        merchant_dict = dict()
        for cart_stock in data:
            # 已支付跳过
            if cart_stock.paid:
                continue

            stock = cart_stock.stock
            # 商品基本信息
            stock_info = {
                'sid': stock.sid,
                'stock_name': stock.stock_name,
                'price': stock.price,
                'sold': stock.sold,
                'type': stock.type,
                'flowers': stock.flowers,
                'material': stock.material,
                'package': stock.package,
                'lof': stock.lof,
                'quantity': cart_stock.quantity,
                'select_state': cart_stock.select_state,
            }

            # 商铺基本信息
            merchant = MerchantStock.objects.get(stock=cart_stock.stock).merchant

            if merchant not in merchant_dict.keys():
                merchant_dict[merchant] = dict()
                merchant_info = merchant_dict[merchant]
                merchant_info['mid'] = merchant.mid
                merchant_info['name'] = merchant.name
                merchant_info['address'] = merchant.address
                merchant_info['register_time'] = merchant.register_time
                # 商家注册人基本信息
                registrant = MerchantRegistrant.objects.get(merchant=merchant).registrant
                merchant_info['uid'] = registrant.uid
                merchant_info['phone'] = registrant.phone
                merchant_info['user_name'] = registrant.user_name
                merchant_info['stock_info'] = [stock_info]
            else:
                merchant_dict[merchant]['stock_info'].append(stock_info)

        # 购物车基本信息
        shop_cart = data[0].shop_cart
        res_data['openid'] = shop_cart.openid
        res_data['total_money'] = shop_cart.total_money
        res_data['select_money'] = shop_cart.select_money
        res_data['num'] = shop_cart.num
        res_data['select_all'] = shop_cart.select_all
        res_data['merchant_info'] = list(merchant_dict.values())         # 购物车包含的商家

        return res_data

    # 复杂查询
    @staticmethod
    def inquire_obj(data_obj):

        if data_obj.openid:
            res = CartStock.objects.filter(shop_cart_id=data_obj.openid)
            total = len(res)
        else:
            res = CartStock.objects.all()
            total = len(res)

        return res, total

    # 数据表修改
    @staticmethod
    def update_model(data_obj):
        # 用户表的添加
        merchant = Merchant.objects.filter(mid=data_obj.mid)
        dict_param = ModelControl.copy_model(Merchant, data_obj)        # 获取写入表的数据
        merchant.update(**dict_param)                                   # 修改&写入

    # 数据表添加
    def add_model(self, data_obj):
        # 购物车购买商品数据表
        shop_cart = ShopCart.objects.get(openid=data_obj.openid)
        stock = Stock.objects.get(sid=data_obj.sid)
        data_obj.shop_cart = shop_cart
        data_obj.stock = stock
        dict_param = ModelControl.copy_model(CartStock, data_obj)
        cart_stock = CartStock(**dict_param)
        cart_stock.save()

        # 刷新购物车
        self.refresh_cart_table(data_obj.openid)

    # 刷新购物车表数据
    @staticmethod
    def refresh_cart_table(openid):
        cart_data = CartStock.objects.filter(shop_cart_id=openid)

        num = 0
        total_money = 0
        select_money = 0
        select_all = True
        for obj in cart_data:

            num += obj.quantity                 # 购物车总数量

            price = Stock.objects.get(sid=obj.stock_id).price       # 商品价格

            # 购物车总价
            total_money += round(price * obj.quantity)

            # 是否选中
            if obj.select_state:
                select_money += round(price * obj.quantity)                 # 选中物件价格
            else:
                select_all = False

        # 刷新购物车数据
        cart = ShopCart.objects.get(openid=openid)
        cart.select_all = select_all
        cart.num = num
        cart.total_money = total_money
        cart.select_money = select_money
        cart.save()




