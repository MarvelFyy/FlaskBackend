from fullstack import app,api,db
from fullstack.utils import to_json
from fullstack.Models.Member import Member
from fullstack.Models.OauthMemberBind import OauthMemberBind
from flask_restful import Resource
from fullstack.utils import paginate
from flask import request,jsonify


# @app.route('/vue/member')
class Members(Resource):
    def get(self):
        # 查询参数
        res=request.values
        query=res['query']
        pagenum=int(res['pagenum'])
        pagesize=int(res['pagesize'])
        ret=paginate(pagenum,pagesize)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++')
        # 查询记录总数
        counts=Member.query.filter_by(status=2).count()

        # query字符串为空
        if not query.strip():
            sql='''
            SELECT* 
            FROM members
            WHERE status=2
            LIMIT {0},{1}
            '''.format(ret['limit'],ret['offset'])

        else:
            sql='''
            SELECT* 
            FROM members
            WHERE nickname LIKE '%%{0}%%' OR mobile LIKE '%%{0}%%'
            '''.format(query)

        result=db.engine.execute(sql)
        responseData=dict()
        jsonData=list()

        for row in result:
            jsonData.append(to_json(Member,row))

        responseData['total']=counts
        # 当前页
        responseData['pagenum']=1
        responseData['members']=jsonData

        return responseData

    def delete(self):
        print(request.values)
        res=request.values
        id=int(res['id'])
        sql='''
        DELETE FROM members
        WHERE id={0}
        '''.format(id)
        result=db.engine.execute(sql)
        # r=dict((zip(result.keys(), result)))
        return jsonify(status=200)
    
    def patch(self):
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        rest=request.json
        id=rest['data']['id']
        nickname=rest['data']['nickname']
        mobile=rest['data']['mobile']
        remain=rest['data']['remain']
        sql='''
        UPDATE members
        SET nickname='{0}',mobile={1},remain={2}
        WHERE id={3}
        '''.format(nickname,mobile,remain,id)
        db.engine.execute(sql)
        return jsonify(status=200)

api.add_resource(Members,'/vue/member')

