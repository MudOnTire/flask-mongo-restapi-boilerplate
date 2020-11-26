import json


def updateDocFields(doc):
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
