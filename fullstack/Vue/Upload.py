import os
import uuid
import qiniu.config
from qiniu import Auth,put_data,BucketManager
from flask import request,jsonify
from fullstack import app,api,db
from flask_restful import Resource
from fullstack.utils import getCurrentTime,to_json

# BASE_URL='http://localhost:5000'

# 初始化
# 在使用SDK前，需要一对有效的AccessKey和SectretKy签名授权
access_key='s6OCt76iiZEkuGd0fq_knhzYYtpwkrn1eN4tJjXB'
secret_key='2HZn8VGhpQga5-jL9faTPO0WjkNQEUk_YHygEZZ6'

#构建鉴权对象
q = Auth(access_key, secret_key)

# 初始化BucketManager 用于删除单个文件
bucket=BucketManager(q)

#要上传的空间
bucket_name = 'vue-flask'


#要上传文件的本地路径


class UploadImages(Resource):
    def post(self):
        # 响应信息
        response={'meta':{'status':200,'msg':'上传成功'},'data':{}}
        files=request.files['file']
        key=str(uuid.uuid1())+'-'+files.filename
        imageName=files.filename
        #生成上传token token失效时间
        token=q.upload_token(bucket_name,key,3600)
        ret,info=put_data(token,key,files.read())
        # 上传后保存的文件名
        print('ret:',ret)
        print('info:',info)
        if info.status_code !=200:
            response['meta']['status']=-1
            response['meta']['msg']='上传失败'
        response['data']['imageName']=imageName
        QINIU_DOMAIN=app.config['QINIU_DOMAIN']
        response['data']['url']=QINIU_DOMAIN+ret.get('key')
        # response['data']['url']='http://q5w0xd46n.bkt.clouddn.com/dcb7c128-5246-11ea-a95f-1063c844e2a2-avatar.png'
        print(response)
        return jsonify(response)
    
    def patch(self):
        res=request.json
        key=res['data']['key']
        # ret,info=bucket.delete(bucket_name,key)
        print(key)
        return jsonify(status=200)

api.add_resource(UploadImages,'/vue/upload')

