from flask_restful import reqparse
from src.common.utils import updateDocFields

# get
get_args = reqparse.RequestParser()
get_args.add_argument("page_index", type=int)
get_args.add_argument("page_size", type=int)

# delete args
delete_args = reqparse.RequestParser()
delete_args.add_argument('ids', action='append')
delete_args.add_argument('soft', type=bool, default=False)


# query api
def query(Model, resource):
    args = get_args.parse_args()
    page_index = args['page_index'] or 1
    page_size = args['page_size'] or 10
    result = []

    db_objs = Model.objects(deleted__ne=True).skip(
        (page_index - 1) * page_size).limit(page_size)
    for db_obj in db_objs:
        obj = updateDocFields(db_obj)
        result.append(obj)
    res = {
        'list': result,
        'pagination': {
            'current': page_index,
            'pageSize': page_size,
            'total': db_objs.count()
        }
    }
    return res, 200


# delete
def delete(Model, resource):
    args = delete_args.parse_args()
    ids = args['ids']
    soft = args['soft']
    targets = Model.objects.filter(id__in=ids)
    for target in targets:
        if soft:
            target['deleted'] = True
            target.save()
        else:
            target.delete()
    return 200


# get single
def get(Model, id, resource):
    target = Model.objects.with_id(id)
    if target is not None:
        obj = updateDocFields(target)
        return obj, 200
    else:
        return 404