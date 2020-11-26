from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from src.common.utils import updateDocFields

from src.models.user import User

# get
get_args = reqparse.RequestParser()
get_args.add_argument("page_index", type=int)
get_args.add_argument("page_size", type=int)

# post
post_args = reqparse.RequestParser()
post_args.add_argument("name",
                       type=str,
                       help="Username is required",
                       required=True)
post_args.add_argument("password",
                       type=str,
                       help="Password is required",
                       required=True)
post_args.add_argument("role", type=str, default="user")

# put
put_args = reqparse.RequestParser()
put_args.add_argument("name", type=str)
put_args.add_argument("password", type=str)
put_args.add_argument("role", type=str)

# delete args
delete_args = reqparse.RequestParser()
delete_args.add_argument('ids', action='append')
delete_args.add_argument('soft', type=bool, default=False)


class UsersApi(Resource):
    # query
    def get(self):
        args = get_args.parse_args()
        page_index = args['page_index'] or 1
        page_size = args['page_size'] or 10
        users = []

        db_users = User.objects(deleted__ne=True).skip(
            (page_index - 1) * page_size).limit(page_size)
        for db_user in db_users:
            user = updateDocFields(db_user)
            users.append(user)
        res = {
            'list': users,
            'pagination': {
                'current': page_index,
                'pageSize': page_size,
                'total': db_users.count()
            }
        }
        return res, 200

    # create
    def post(self):
        args = post_args.parse_args()
        hashed_pass = generate_password_hash(args['password'])
        new_user = User(name=args['name'],
                        password=hashed_pass,
                        role=args['role'])
        saved = new_user.save()
        user = updateDocFields(saved)
        return user, 201

    # delete
    def delete(self):
        args = delete_args.parse_args()
        ids = args['ids']
        soft = args['soft']
        targets = User.objects.filter(id__in=ids)
        for target in targets:
            if soft:
                target['deleted'] = True
                target.save()
            else:
                target.delete()
        return 200


class UserApi(Resource):
    # update
    def put(self, id):
        args = put_args.parse_args()
        target = User.objects.with_id(id)
        for key, value in args.items():
            if value is not None:
                if key == 'password':
                    target['password'] = generate_password_hash(value)
                else:
                    target[key] = value
        saved = target.save()
        user = updateDocFields(saved)
        return user, 200

    # get single
    def get(self, id):
        target = User.objects.with_id(id)
        if target is not None:
            user = updateDocFields(target)
            return user, 200
        else:
            return 404