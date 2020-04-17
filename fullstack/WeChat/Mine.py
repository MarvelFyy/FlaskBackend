import json
import requests
import decimal
from flask import Flask, jsonify, Response
from flask import request, g
from fullstack import app, api, db
from flask_restful import Resource
from fullstack.Models.PaymentOrder import PaymentOrder
from fullstack.Models.PaymentOrderItem import PaymentOrderItem
from fullstack.Models.Food import Food
from fullstack.utils import getCurrentTime, getDictFilterField, selectFilterObj


class MineOrders(Resource):
    def get(self):
        response = {'code': 200, 'msg': '操作成功', 'data': {}}
        member_info = g.member_info
        res = request.values
        status = int(res['status']) if 'status' in res else 0
        query = PaymentOrder.query.filter_by(member_id=member_info.id)
        # 等待付款
        if status == -8:
            query = query.filter(PaymentOrder.status == -8)

        # 待发货
        elif status == -7:
            query = query.filter(
                PaymentOrder.status == 1, PaymentOrder.express_status == -7, PaymentOrder.comment_status == 0)
        # 待确定
        elif status == -6:
            query = query.filter(
                PaymentOrder.status == 1, PaymentOrder.express_status == -6, PaymentOrder.comment_status == 0)
        # 待评价
        elif status == -5:
            query = query.filter(
                PaymentOrder.status == 1, PaymentOrder.express_status == 1, PaymentOrder.comment_status == 0)
        # 已完成
        elif status == 1:
            query = query.filter(
                PaymentOrder.status == 1, PaymentOrder.express_status == 1, PaymentOrder.comment_status == 1)
        else:
            query = query.filter(PaymentOrder.status == 0)

        pay_order_list = query.order_by(PaymentOrder.id.desc()).all()
        data_pay_order_list = []
        if pay_order_list:
            pay_order_ids = selectFilterObj(pay_order_list, "id")
            pay_order_item_list = PaymentOrderItem.query.filter(
                PaymentOrderItem.pay_order_id.in_(pay_order_ids)).all()
            food_ids = selectFilterObj(pay_order_item_list, "food_id")
            food_map = getDictFilterField(Food, Food.id, "id", food_ids)
            pay_order_item_map = {}
            if pay_order_item_list:
                for item in pay_order_item_list:
                    if item.pay_order_id not in pay_order_item_map:
                        pay_order_item_map[item.pay_order_id] = []

                    tmp_food_info = food_map[item.food_id]
                    pay_order_item_map[item.pay_order_id].append({
                        'id': item.id,
                        'food_id': item.food_id,
                        'quantity': item.quantity,
                        'price': str(item.price),
                        'pic_url': tmp_food_info.imageURL,
                        'name': tmp_food_info.name
                    })

            for item in pay_order_list:
                tmp_data = {
                    'status': item.pay_status,
                    'status_desc': item.status_desc,
                    'date': item.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'order_number': item.order_number,
                    'order_sn': item.order_sn,
                    'note': item.note,
                    'total_price': str(item.total_price),
                    'goods_list': pay_order_item_map[item.id]
                }
                print(item.id)

                data_pay_order_list.append(tmp_data)

        response['data']['pay_order_list'] = data_pay_order_list
        return jsonify(response)


api.add_resource(MineOrders, '/wechat/api/mine/order')
