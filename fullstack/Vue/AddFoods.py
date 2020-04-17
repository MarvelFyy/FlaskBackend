import decimal
from flask import request,jsonify
from fullstack import app,api,db
from flask_restful import Resource
from fullstack.Models.Food import Food
from fullstack.utils import getCurrentTime,to_json

class AddFoods(Resource):
    def post(self):
        response={'meta':{'status':200,'msg':'添加成功'}}
        rest=request.json.get('data')
        food=Food()
        food.category=rest['category']
        food.name=rest['name']
        food.priced=decimal.Decimal(rest['priced']) 
        food.price=decimal.Decimal(rest['price']) 
        food.stock=int(rest['stock'])
        food.description=rest['description']
        food.imageName=rest['imageName']
        food.imageURL=rest['imageURL']
        food.status=0  # status 0:未上架 1:已上架
        food.cover=0 #是否设为封面
        food.month_count=0 #月销售量
        food.total_count=0 #总销售量
        food.view_count=0 #总浏览量
        food.comment_count=0 #总评论量
        food.updated_time=food.created_time=getCurrentTime()
        db.session.add(food)
        db.session.commit()
        return jsonify(response)

api.add_resource(AddFoods,'/vue/addfoods')