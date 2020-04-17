import json,requests
from flask import Flask,jsonify,Response
from flask import request,session,g
from fullstack import app,api,db
from flask_restful import Resource
from fullstack.Models.Member import Member
from fullstack.Models.ShareHistory import ShareHistory
from fullstack.utils import getCurrentTime


class MemberShares(Resource):
    def post(self):
        print('进来了')
        response={'code':200,'msg':'操作成功','data':{}}
        res=request.values
        url=res['url'] if 'url' in res else ''
        member_info=g.member_info
        print(g.member_info)
        share=ShareHistory()
        if member_info:
            share.member_id=member_info.id
        share.share_url=url
        share.created_time=getCurrentTime()
        db.session.add(share)
        db.session.commit()
        return jsonify(response)

api.add_resource(MemberShares,'/wechat/api/member/share')