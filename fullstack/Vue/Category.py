from flask import request,jsonify
from fullstack import app,api,db
from flask_restful import Resource
from fullstack.Models.Category import Category
from fullstack.utils import getCurrentTime,to_json,paginate




class Categorys(Resource):
    def post(self):
        rest=request.json    
        category=Category()
        category.name=rest['data']['name']
        category.updated_time=category.created_time=getCurrentTime()
        db.session.add(category)
        db.session.commit()

        return jsonify(status=200)
    
    def get(self):
        sql='''
        SELECT*
        FROM category
        '''
        result=db.engine.execute(sql)
        jsonData=list()
        for row in result:
            jsonData.append(to_json(Category,row))
        
        return jsonData

api.add_resource(Categorys,'/vue/category')

class Categories(Resource):
    def get(self):
        # 查询参数
        res=request.values
        query=res['query']
        pagenum=int(res['pagenum'])
        pagesize=int(res['pagesize'])
        ret=paginate(pagenum,pagesize)
        flag=True
        print('++++++++++++++++++++++++++++++++++++++++++++++++++')
        

        # query字符串为空
        if not query.strip():
            sql='''
            SELECT* 
            FROM category
            LIMIT {0},{1}
            '''.format(ret['limit'],ret['offset'])
            counts=Category.query.count()

        else:
            sql='''
            SELECT* 
            FROM category
            WHERE name LIKE '%%{0}%%'
            '''.format(query)
            flag=False

        result=db.engine.execute(sql)
        responseData=dict()
        jsonData=list()

        for row in result:
            jsonData.append(to_json(Category,row))
        
        if not flag:
            counts=len(jsonData)

        responseData['total']=counts
        # 当前页
        responseData['pagenum']=1
        responseData['categories']=jsonData

        return responseData

    def delete(self):
        res=request.values
        id=int(res['id'])
        sql='''
        DELETE FROM category
        WHERE id={0}
        '''.format(id)
        result=db.engine.execute(sql)
        # r=dict((zip(result.keys(), result)))
        return jsonify(status=200)
    
    def patch(self):
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        rest=request.json.get('data')
        id=int(rest['id'])
        category=Category.query.get(id)
        category.name=rest['name']
        category.updated_time=getCurrentTime()
        db.session.commit()
        return jsonify(status=200)

api.add_resource(Categories,'/vue/categories')