import json
import datetime
import math
import decimal
from flask import jsonify


def getCurrentTime(format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(format)


# 重写json序列化类
# 继承json.JSONDecoder
class MultiEnCoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")

        elif isinstance(obj, decimal.Decimal):
            return float(obj)

        else:
            return json.JSONEncoder.default(self, obj)

# 生成json
# json.dumps无法对字典中的datetime时间格式进行转化。


def to_json(col, row):
    result = dict()
    '''
     获取表里面的列并存到字典里面
     '''
    for c, s in zip(col.__table__.columns, row):
        result[c.name] = s

    return json.dumps(result, cls=MultiEnCoder)


def paginate(pagenum, pagesize):
    pass
    '''
     表分页
     '''
    if pagenum > 0:
        pagenum -= 1

    return{
        'limit': pagenum*pagesize,
        'offset': pagesize
    }


'''
根据某个字段获取一个dict出来
'''


def getDictFilterField(db_model, select_filed, key_field, id_list):
    ret = {}
    query = db_model.query
    if id_list and len(id_list) > 0:
        query = query.filter(select_filed.in_(id_list))

    list = query.all()
    if not list:
        return ret
    for item in list:
        if not hasattr(item, key_field):
            break

        ret[getattr(item, key_field)] = item
    return ret


def selectFilterObj(obj, field):
    ret = []
    for item in obj:
        if not hasattr(item, field):
            break
        if getattr(item, field) in ret:
            continue
        ret.append(getattr(item, field))
    return ret


def getDictListFilterField(db_model, select_filed, key_field, id_list):
    ret = {}
    query = db_model.query
    if id_list and len(id_list) > 0:
        query = query.filter(select_filed.in_(id_list))

    list = query.all()
    if not list:
        return ret
    for item in list:
        if not hasattr(item, key_field):
            break
        if getattr(item, key_field) not in ret:
            ret[getattr(item, key_field)] = []

        ret[getattr(item, key_field)].append(item)
    return ret
