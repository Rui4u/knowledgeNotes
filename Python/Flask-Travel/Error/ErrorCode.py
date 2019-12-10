class api_request_type():
    successed = 200
    failure = -200
    user_cant_find = -502
    user_cant_find_by_id = -503
    failure_no_pars = -504


def errortostring(req_status):
    message = ''
    # 判断状态码 返回message
    if req_status == api_request_type.successed:
        message = '操作成功'
    elif req_status == api_request_type.user_cant_find:
        message = '此姓名、手机号无对应嘉宾,请联系管理员'
    elif req_status == api_request_type.user_cant_find_by_id:
        message = '此id无对应嘉宾,请联系管理员'
    elif req_status == api_request_type.failure_no_pars:
        message = '参数错误'
    elif req_status == api_request_type.failure:
        message = '操作失败'
    else:
        message = '未知错误'
    return message
