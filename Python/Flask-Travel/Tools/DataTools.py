from Error.ErrorCode import *
from flask import jsonify


def serialize(model):
    if isinstance(model, int):
        return model
    else:
        from sqlalchemy.orm import class_mapper
        columns = [c.key for c in class_mapper(model.__class__).columns]
        dicts = dict((c, getattr(model, c)) for c in columns)
        return dicts

def serializelist(models):
    data = []
    for model in models:
        data.append(serialize(model))
    return data


def backjson(resp):

    print('开始解析')

    data = {}
    req_status = api_request_type.failure
    message = ''

    print(type(resp))

    if isinstance(resp, list):
        resp_array = []
        for item in resp:
            resp_array.append(serialize(item))
        data = resp_array
        req_status = api_request_type.successed
    elif type(resp)is dict:
        data = resp
        req_status = api_request_type.successed
    elif isinstance(resp, int):
        data = {}
        req_status = resp
    else:
        data = {}
        req_status = api_request_type.failure

    message = errortostring(req_status)

    deal_resp = {
        'meta': {'status': req_status, 'message': message},
        'data': data
            }
    json = jsonify(deal_resp)
    print(deal_resp)
    print('结束解析')

    return json

