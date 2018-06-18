import json

def json_data(url, msg, code=1):
    data = {
        'code' : code,
        'msg' : msg,
        'url' : url
    }
    return json.dumps(data)