import decimal
from fullstack import app,api,db
from fullstack.utils import to_json
from fullstack.Models.Food import Food
from fullstack.Models.OauthMemberBind import OauthMemberBind
from flask_restful import Resource
from fullstack.utils import paginate,getCurrentTime
from flask import request,jsonify

class Foods(Resource):
    def get(self):
        # 查询参数
        res=request.values
        query=res['query']
        status=query
        print(type(query))
        if not is_number(query):
            status=-1
        pagenum=int(res['pagenum'])
        pagesize=int(res['pagesize'])
        ret=paginate(pagenum,pagesize)
        flag=True
        print('++++++++++++++++++++++正在访问Foods++++++++++++++++++++++++++++')

        # query字符串为空
        if not query.strip():
            sql='''
            SELECT* 
            FROM food
            LIMIT {0},{1}
            '''.format(ret['limit'],ret['offset'])
            counts=Food.query.count()

        else:
            sql='''
            SELECT* 
            FROM food
            WHERE category='{0}' OR status={1} OR name LIKE '%%{0}%%'  
            '''.format(query,status)
            flag=False
            print(status)
        #  OR status='{0}' 

        result=db.engine.execute(sql)
        responseData=dict()
        jsonData=list()
        for row in result:
            jsonData.append(to_json(Food,row))
        
        if not flag:
            counts=len(jsonData)

        responseData['total']=counts
        # 当前页
        responseData['pagenum']=1
        responseData['foods']=jsonData

        return responseData

    def post(self):
        response={'meta':{'status':200,'msg':'修改成功'}}
        rest=request.json.get('data')
        status=int(rest['status']) if 'status' in rest else 0
        cover=int(rest['cover']) if 'cover' in rest else 0
        id=int(rest['id'])
        food=Food.query.get(id)
        food.category=rest['category']
        food.name=rest['name']
        food.priced=decimal.Decimal(rest['priced'])
        food.price=decimal.Decimal(rest['price'])
        food.stock=int(rest['stock'])
        food.status=status
        food.cover=cover
        food.imageName=rest['imageName']
        food.imageURL=rest['imageURL']
        food.description=rest['description']
        food.updated_time=getCurrentTime()
        db.session.commit()
        return jsonify(response)
    
    def delete(self):
        print(request.values)
        res=request.values
        id=int(res['id'])
        sql='''
        DELETE FROM food
        WHERE id={0}
        '''.format(id)
        result=db.engine.execute(sql)
        return jsonify(status=200)
    
    def patch(self):
        rest=request.json.get('data')
        id=int(rest['id'])
        status=int(rest['status']) if 'status' in rest else None
        cover=int(rest['cover']) if 'cover' in rest else None
        print(status)
        print(cover)
        if not status==None:
            print('上架')
            sql='''
            UPDATE food
            SET status={0}
            WHERE id={1}
            '''.format(status,id)
            db.engine.execute(sql)

        
        if not cover==None:
            print('设置了封面')
            sql='''
            UPDATE food
            SET cover={0}
            WHERE id={1}
            '''.format(cover,id)
            db.engine.execute(sql)

        return jsonify(status=200)

api.add_resource(Foods,'/vue/foods')

# 根据状态筛选
class Status(Resource):
    def post(self):
        pass

api.add_resource(Status,'/vue/status')

def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包
        for i in s:
            unicodedata.numeric(i)  # 把一个表示数字的字符串转换为浮点数返回的函数
            #return True
        return True
    except (TypeError, ValueError):
        pass
    return False