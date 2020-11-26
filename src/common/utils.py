import json


def liftDocId(doc):
    docObj = json.loads(doc.to_json())
    id = docObj["_id"]["$oid"]
    docObj["id"] = id
    del docObj["_id"]
    return docObj
