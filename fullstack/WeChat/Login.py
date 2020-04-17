import json
import requests
from flask import Flask, jsonify, Response
from flask import request, session
from fullstack import app, api, db
from flask_restful import Resource
from fullstack.Models.Member import Member
from fullstack.Models.OauthMemberBind import OauthMemberBind
from fullstack.utils import getCurrentTime
from fullstack.WeChat.Service.MemberService import MemberService


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    return jsonify('Hello,WeChat')


class LoginWechat(Resource):
    def post(self):
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        req = request.values
        code = req['code'] if 'code' in req else ''
        if not code or len(code) < 1:
            resp['code'] = -1
            resp['msg'] = "需要code"
            return jsonify(resp)

        openid = MemberService.getWeChatOpenId(code)
        if openid is None:
            resp['code'] = -1
            resp['msg'] = '出错'
            return jsonify(resp)
        nickname = req['nickName'] if 'nickName' in req else ''
        sex = req['gender'] if 'gender' in req else 0
        avatar = req['avatarUrl'] if 'avatarUrl' in req else ''

        app.logger.info(nickname)
        app.logger.info(sex)
        app.logger.info(avatar)
        """
            判断是否已经登录
        """
        bind_info = OauthMemberBind.query.filter_by(
            openid=openid, type=1).first()
        if not bind_info:

            model_member = Member()
            model_member.nickname = nickname
            model_member.sex = sex
            model_member.mobile = ''
            model_member.avatar = avatar
            model_member.salt = MemberService.geneSalt()
            model_member.reg_ip = ''
            model_member.status = 1
            model_member.remain = 0
            model_member.updated_time = model_member.created_time = getCurrentTime()
            db.session.add(model_member)
            db.session.commit()

            model_bind = OauthMemberBind()
            model_bind.member_id = model_member.id
            model_bind.client_type = ''
            model_bind.type = 1
            model_bind.openid = openid
            model_bind.unionid = ''
            model_bind.extra = ''
            model_bind.updated_time = model_bind.created_time = getCurrentTime()
            db.session.add(model_bind)
            db.session.commit()

            bind_info = model_bind

        member_info = Member.query.filter_by(id=bind_info.member_id).first()
        # 产生token
        token = "%s#%s" % (MemberService.geneAuthCode(
            member_info), member_info.id)
        resp['data'] = {'token': token}
        print(resp)
        return jsonify(resp)


api.add_resource(LoginWechat, '/wechat/login')


class CheckWechat(Resource):
    def post(self):
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        req = request.values
        code = req['code'] if 'code' in req else ''
        if not code or len(code) < 1:
            resp['code'] = -1
            resp['msg'] = "需要code"
            return jsonify(resp)

        openid = MemberService.getWeChatOpenId(code)
        if openid is None:
            resp['code'] = -1
            resp['msg'] = '出错'
            return jsonify(resp)

        bind_info = OauthMemberBind.query.filter_by(
            openid=openid, type=1).first()
        if not bind_info:
            print('判断了bindinfo')
            resp['code'] = -1
            resp['msg'] = '未绑定'
            return jsonify(resp)

        member_info = Member.query.filter_by(id=bind_info.member_id).first()
        if not member_info:
            resp['code'] = -1
            resp['msg'] = '未查询到绑定信息'
            return jsonify(resp)

        # 产生token
        token = "%s#%s" % (MemberService.geneAuthCode(
            member_info), member_info.id)
        resp['data'] = {'token': token}
        return jsonify(resp)


api.add_resource(CheckWechat, '/wechat/check')
