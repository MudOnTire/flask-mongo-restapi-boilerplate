from datetime import datetime
from flask_restful import reqparse, abort, wraps, Resource
from src.common.utils import updateDocFields, verifyToken
from src.models.user import User

# get
get_args = reqparse.RequestParser()
get_args.add_argument("page_index", type=int)
get_args.add_argument("page_size", type=int)

# delete args
delete_args = reqparse.RequestParser()
delete_args.add_argument('ids', action='append')
delete_args.add_argument('soft', type=bool, default=False)

# auth
auth_args = reqparse.RequestParser()
auth_args.add_argument('token', location='cookies')


# query
def query(Model, resource, doc_modifier=updateDocFields):
    args = get_args.parse_args()
    page_index = args['page_index'] or 1
    page_size = args['page_size'] or 10
    result = []

    db_objs = Model.objects(deleted__ne=True).skip(
        (page_index - 1) * page_size).limit(page_size)
    for db_obj in db_objs:
        obj = doc_modifier(db_obj)
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
def get(Model, id, resource, doc_modifier=updateDocFields):
    target = Model.objects.with_id(id)
    if target is not None:
        obj = doc_modifier(target)
        return obj, 200
    else:
        return 404

# update
def update(target, args, doc_modifier=updateDocFields):
    for key, value in args.items():
        if value is not None:
            target[key] = value
    target['updatedTime'] = datetime.utcnow()
    saved = target.save()
    obj = doc_modifier(saved)
    return obj, 200


def basic_authentication(*args, **kwargs):
    args = auth_args.parse_args()
    if 'token' not in args:
        return
    token = args['token']
    info = verifyToken(token)
    if info is None:
        return
    if 'id' in info:
        id = info['id']
        db_user = User.objects.with_id(id)
        return updateDocFields(db_user)


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)
        account = basic_authentication()

        if account:
            kwargs['account'] = account
            return func(*args, **kwargs)
        abort(401)

    return wrapper


class AuthResource(Resource):
    method_decorators = [authenticate]
