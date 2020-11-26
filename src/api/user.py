import logging
from flask_restful import Resource, reqparse
from src.common.utils import liftDocId

from models.user import User

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
            user = liftDocId(db_user)
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
        new_user = User(name=args['name'],
                        password=args['password'],
                        role=args['role'])
        saved = new_user.save()
        return liftDocId(saved), 201