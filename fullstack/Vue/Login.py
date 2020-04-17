import json
from flask import Flask, jsonify,Response,session
from flask import request,redirect,url_for,session
from fullstack.Models.Admin import Admin
from fullstack import app,api,db
from flask_restful import Resource


# @app.route('/login',methods=["POST"])
# def login():
#     if request.method=='POST':
#         print('请求登录')
#         data=json.loads(request.data)
#         username=data['username']
#         password=data['password']
#         # 查询数据库
#         admin=Admin.query.first()        
#         # 验证同户名和密码是否一致
#         if admin.username==username and Admin.check_password(admin,password):
#             return jsonify(status=200)
#         else:
#             return jsonify(status=400)

class LoginVue(Resource):
    def post(self):
        print('请求登录')
        data=json.loads(request.data)
        username=data['username']
        password=data['password']
        session['username']=username
        # 设置session过期时间 一个月
        session.permanent=True
        # 查询数据库
        admin=Admin.query.first()        
        # 验证同户名和密码是否一致
        if admin.username==username and Admin.check_password(admin,password):
            return jsonify(status=200)
        else:
            return jsonify(status=400)
        

api.add_resource(LoginVue,'/login')

# 测试用
class Test(Resource):
    def get(self):
        sql="SELECT * FROM admin"
        result=db.engine.execute(sql)
        for row in result:
            app.logger.info(row)

api.add_resource(Test,'/test')