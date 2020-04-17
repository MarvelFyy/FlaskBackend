import json
import requests
import decimal
from flask import Flask, jsonify, Response
from flask import request, g
from fullstack import app, api, db
from flask_restful import Resource
from fullstack.Models.Member import Member
from fullstack.Models.Food import Food
from fullstack.Models.OauthMemberBind import OauthMemberBind
from fullstack.Models.PaymentOrder import PaymentOrder
from fullstack.utils import getCurrentTime, getDictFilterField, selectFilterObj
from fullstack.WeChat.Service.CartService import CartService
from fullstack.WeChat.Service.FoodService import FoodService
from fullstack.Models.ShoppingCart import ShoppingCart
from fullstack.WeChat.Service.PaymentService import PaymentService


# 订单信息
class OrderInfo(Resource):
    def post(self):
        response = {'code': 200, 'msg': '操作成功', 'data': {}}
        res = request.values
        params_goods = res['goods'] if 'goods' in res else None
        member_info = g.member_info
        params_goods_list = []
        if params_goods:
            params_goods_list = json.loads(params_goods)

        food_dic = {}
        for item in params_goods_list:
            food_dic[item['id']] = item['number']

        food_ids = food_dic.keys()
        food_list = Food.query.filter(Food.id.in_(food_ids)).all()
        data_food_list = []
        # 运费
        yun_price = pay_price = decimal.Decimal(0.00)

        if food_list:
            for item in food_list:
                temp = {
                    "id": item.id,
                    "name": item.name,
                    "price": str(item.price),
                    "pic_url": item.imageURL,
                    "number": food_dic[item.id]
                }
                pay_price = pay_price+item.price*int(food_dic[item.id])
                data_food_list.append(temp)

        default_address = {
            "name": '萌太其',
            "mobile": "15730615013",
            "address": "重庆万州"
        }

        response['data']['food_list'] = data_food_list
        response['data']['pay_price'] = str(pay_price)
        response['data']['yun_price'] = str(yun_price)
        response['data']['total_price'] = str(pay_price+yun_price)
        response['data']['default_address'] = default_address

        return jsonify(response)


api.add_resource(OrderInfo, '/wechat/api/order/info')

# 订单提交


class OrderCreate(Resource):
    def post(self):
        response = {'code': 200, 'msg': '操作成功', 'data': {}}
        res = request.values
        type = res['type'] if 'type' in res else ''
        params_goods = res['goods'] if 'goods' in res else None

        items = []
        if params_goods:
            items = json.loads(params_goods)

        if len(items) < 1:
            response['code'] = -1
            response['msg'] = '未登录，获取失败'
            return jsonify(response)

        member_info = g.member_info
        target = PaymentService()
        params = {}
        print(member_info.id)
        response = target.createOrder(member_info.id, items, params)
        print('进来了')
        if response['code'] == 200 and type == "cart":
            CartService.deleteItem(member_info.id, items)
        return jsonify(response)


api.add_resource(OrderCreate, '/wechat/api/order/create')

# 支付


class OrderPay(Resource):
    def post(self):
        response = {'code': 200, 'msg': '操作成功', 'data': {}}
        # res = request.values
        # member_info = g.member_info
        # order_sn = res['order_sn'] if 'order_sn' in res else ''
        # pay_order_info = PaymentOrder.query.filter_by( order_sn = order_sn,member_id = member_info.id ).first()
        # if not pay_order_info:
        #     response['code']=-1
        #     response['msg']="系统繁忙。请稍后再试~"
        #     return jsonify(response)
        
	    # oauth_bind_info = OauthMemberBind.query.filter_by( member_id =  member_info.id ).first()

        # if not oauth_bind_info:
        #     response['code']=-1
        #     response['msg']="系统繁忙。请稍后再试~"
        #     return jsonify(response)

        # config_mina=app
        return jsonify(response)

api.add_resource(OrderPay, '/wechat/api/order/pay')
