import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


# instantiate the app
app = Flask(__name__)

# 加载配置文件
app.config.from_object('fullstack.settings.ProductionConfig')
# 配置secret_key

# 数据库
db=SQLAlchemy(app)

# enable CORS 用于http跨域
CORS(app, resources={r'/*': {'origins': '*'}})

# 用Api来绑定app
api=Api(app)

# 检查当前模块是否是主模块
if __name__ == '__main__':
    app.run()

# 为了避免循环依赖 在此导入模块
import fullstack.Models,fullstack.commands

# 实验室后台管理系统
import fullstack.Vue

# 微信小程序
import fullstack.WeChat

#拦截器
import fullstack.Interceptors