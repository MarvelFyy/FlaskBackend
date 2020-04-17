import json
import requests
from flask import Flask, jsonify, Response
from flask import request, g
from fullstack import app, api, db
from flask_restful import Resource
from fullstack.Models.Member import Member
from fullstack.Models.ShareHistory import ShareHistory
from fullstack.Models.Food import Food
from fullstack.utils import getCurrentTime, getDictFilterField, selectFilterObj
from fullstack.WeChat.Service.CartService import CartService
from fullstack.Models.ShoppingCart import ShoppingCart


class ShoppingSet(Resource):
    def post(self):
        response = {'code': 200, 'msg': '操作成功', 'data': {}}
        res = request.values
        id = int(res['id']) if 'id' in res else 0
        number = int(res['number']) if 'number' in res else 0
        if id < 1 or number < 1:
            response['code'] = -1
            response['msg'] = '添加购物车失败'
            return jsonify(response)

        member_info = g.member_info
        if not member_info:
            response['code'] = -1
            response['msg'] = '添加购物车失败'
            return jsonify(response)

        food = Food.query.filter_by(id=id).first()
        if not food:
            response['code'] = -1
            response['msg'] = '添加购物车失败'
            return jsonify(response)

        if food.stock < number:
            response['code'] = -1
            response['msg'] = '添加购物车失败,库存不足'
            return jsonify(response)

        ret = CartService.setItems(
            member_id=member_info.id, food_id=id, number=number)
        if not ret:
            response['code'] = -1
            response['msg'] = '添加购物车失败'
            return jsonify(response)

        return jsonify(response)

    def delete(self):
        response = {'code': 200, 'msg': '操作成功', 'data': {}}
        res = request.values
        params_goods = res['goods'] if 'goods' in res else None

        items = list()
        if params_goods:
            items = json.loads(params_goods)
            print(items)

        if not items or len(items) < 1:
            return jsonify(response)

        # 验证会员信息
        member_info = g.member_info
        if not member_info:
            response['code'] = -1
            response['msg'] = '删除购物车失败'
            return jsonify(response)

        ret = CartService.deleteItem(member_id=member_info.id, items=items)

        if not ret:
            response['code'] = -1
            response['msg'] = '删除购物车失败'
            return jsonify(response)

        return jsonify(response)


api.add_resource(ShoppingSet, '/wechat/api/shopping/set')


class ShoppingCarts(Resource):
    def get(self):
        response = {'code': 200, 'msg': '操作成功', 'data': {}}
        member_info = g.member_info
        if not member_info:
            response['code'] = -1
            response['msg'] = '未登录，获取失败'
            return jsonify(response)

        cartResult = ShoppingCart.query.filter_by(
            member_id=member_info.id).all()
        cartList = list()

        if cartResult:
            food_ids = selectFilterObj(cartResult, "food_id")
            food_map = getDictFilterField(Food, Food.id, "id", food_ids)
            for item in cartResult:
                tmp_food_info = food_map[item.food_id]
                temp = {
                    "id": item.id,
                    "number": item.quantity,
                    "food_id": item.food_id,
                    "name": tmp_food_info.name,
                    "price": str(tmp_food_info.price),
                    "pic_url": tmp_food_info.imageURL,
                    "active": True
                }
                cartList.append(temp)

        response['data']['list'] = cartList
        return jsonify(response)


api.add_resource(ShoppingCarts, '/wechat/api/shopping/cart')
