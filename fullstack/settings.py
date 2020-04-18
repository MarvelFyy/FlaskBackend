import os
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
        # 生成密匙
    SECRET_KEY = os.urandom(24)
    DEBUG = True
    # 配置数据库的地址
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/vue_flask'
    # 跟踪数据库的修改 不建议开启
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 七牛云
    QINIU_DOMAIN = 'http://cdn.fyy.cool/'

    # 微信小程序
    WX_APP = {
        'appid': 'wx15f20e174be245b4',
        'appkey': 'a2b1e3e809e40d0182c96f9e03824773'
    }
    API_IGNORE_URLS = [
        "^/api"
    ]
    PAY_STATUS_MAPPING = {
        "1": "已支付",
        "-8": "待支付",
        "0": "已关闭"
    }

    PAY_STATUS_DISPLAY_MAPPING = {
        "0": "订单关闭",
        "1": "支付成功",
        "-8": "待支付",
        "-7": "待发货",
        "-6": "待确认",
        "-5": "待评价"
    }


class DevelopmentConfig(Config):
    # 生成密匙
    SECRET_KEY = os.urandom(24)
    DEBUG = True
    # 配置数据库的地址
    SQLALCHEMY_DATABASE_URI = 'mysql://PRIVATE@Link2046:root@127.0.0.1/vue_flask'
    # 跟踪数据库的修改 不建议开启
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 七牛云
    QINIU_DOMAIN = 'http://cdn.fyy.cool/'

    # 微信小程序
    WX_APP = {
        'appid': 'wx15f20e174be245b4',
        'appkey': 'a2b1e3e809e40d0182c96f9e03824773'
    }
    API_IGNORE_URLS = [
        "^/api"
    ]
    PAY_STATUS_MAPPING = {
        "1": "已支付",
        "-8": "待支付",
        "0": "已关闭"
    }

    PAY_STATUS_DISPLAY_MAPPING = {
        "0": "订单关闭",
        "1": "支付成功",
        "-8": "待支付",
        "-7": "待发货",
        "-6": "待确认",
        "-5": "待评价"
    }


class TestingConfig(Config):
    TESTING = True
