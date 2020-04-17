import json
import requests
from flask import Flask, jsonify, request, g
from sqlalchemy import or_
from fullstack import app, api, db
from flask_restful import Resource
from fullstack.Models.Member import Member
from fullstack.Models.Category import Category
from fullstack.Models.Food import Food
from fullstack.Models.ShoppingCart import ShoppingCart
from fullstack.Models.OauthMemberBind import OauthMemberBind
from fullstack.utils import getCurrentTime
from werkzeug.datastructures import CombinedMultiDict, MultiDict


class FoodIndex(Resource):
    def get(self):
        response = {'code': 200, 'msg': '操作成功', 'data': {}}
        categoryResult = Category.query.all()
        categoryList = list()
        categoryList.append({
            'id': 0,
            'name': '全部'
        })
        if categoryResult:
            for item in categoryResult:
                temp = {
                    'id': item.id,
                    'name': item.name
                }
                categoryList.append(temp)

        # 轮播图选择
        bannerResult = Food.query.filter_by(status=1, cover=1).order_by(
            Food.total_count.desc()).limit(4).all()
        bannerList = list()
        if bannerResult:
            for item in bannerResult:
                temp = {
                    'id': item.id,
                    'pic_url': item.imageURL
                }
                bannerList.append(temp)

        response['data']['categoryList'] = categoryList
        response['data']['bannerList'] = bannerList
        return jsonify(response)


api.add_resource(FoodIndex, '/wechat/food/index')


class FoodSearch(Resource):
    def get(self):
        response = {'code': 200, 'msg': '操作成功', 'data': {}}
        # 查询参数
        res = request.values
        category_name = res['category_name'] if res['category_name'] != '全部' else ''
        match_search = res['match_search']
        p = int(res['p']) if 'p' in res else 1
        query = Food.query.filter_by(status=1)
        if p < 1:
            p = 1

        pagesize = 10
        offset = (p-1)*pagesize

        if category_name.strip():
            query = query.filter(Food.category == category_name)

        if match_search.strip():
            query = Food.query.filter(
                Food.name.like('%%{0}%%'.format(match_search)))

        foodResult = query.order_by(Food.total_count.desc(), Food.id.desc()).offset(
            offset).limit(pagesize).all()
        # foodResult=query
        foodList = list()
        if foodResult:
            for item in foodResult:
                temp = {
                    'id': item.id,
                    'name': item.name,
                    'price': str(item.price),
                    'priced': str(item.priced),
                    'pic_url': item.imageURL,

                }
                foodList.append(temp)

        response['data']['list'] = foodList
        response['data']['hasMore'] = 0 if len(foodList) < pagesize else 1
        print(response['data']['hasMore'])

        return jsonify(response)


api.add_resource(FoodSearch, '/wechat/food/search')


# 商品详情
class FoodDetail(Resource):
    def get(self):
        response = {'code': 200, 'msg': '操作成功', 'data': {}}
        res = request.values
        id = int(res['id']) if 'id' in res else 0
        detail = Food.query.filter_by(id=id).first()
        if not detail or not detail.status:
            response['code'] = -1
            response['msg'] = '商品已下架'
            return jsonify(response)

        member_info = g.member_info
        cart_number = 0
        if member_info:
            cart_number = ShoppingCart.query.filter_by(
                member_id=member_info.id).count()

        response['data']['detail'] = {
            'id': detail.id,
            'name': detail.name,
            'price': str(detail.price),
            'stock': detail.stock,
            'main_image': detail.imageURL,
            'pics': [detail.imageURL],
            'summary': detail.description,
            'total_count': detail.total_count,
            'comment_count': detail.comment_count,
        }
        response['data']['cart_number'] = cart_number
        print(cart_number)
        return jsonify(response)


api.add_resource(FoodDetail, '/wechat/api/food/detail')
