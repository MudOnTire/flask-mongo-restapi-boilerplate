import json
import jwt
import datetime

secret = 'Simple is better than complex'


def updateDocFields(doc):
    if doc is None:
        return None
    dic = json.loads(doc.to_json())
    # id
    id = dic["_id"]["$oid"]
    dic["id"] = id
    del dic["_id"]
    # date
    created = dic["createdTime"]["$date"]
    dic["createdTime"] = created
    updated = dic["updatedTime"]["$date"]
    dic["updatedTime"] = updated
    # deleted
    del dic["deleted"]
    # cls
    del dic["_cls"]
    # password
    if 'password' in dic:
        del dic['password']
    return dic


def createToken(id):
    token = jwt.encode(
        {
            'id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        secret,
        algorithm='HS256').decode('utf-8')
    return token


def verifyToken(token):
    try:
        return jwt.decode(token, secret, algorithm=['HS256'])
    except Exception as e:
        print('verify token failed', e)