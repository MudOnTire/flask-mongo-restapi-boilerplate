from datetime import datetime
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from src.common.utils import updateDocFields

from src.models.user import User
from src.api.base import query, delete, get


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

class UsersApi(Resource):
    # query
    def get(self):
        return query(User, self)

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
        return delete(User, self)


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
        target['updatedTime'] = datetime.utcnow()
        saved = target.save()
        user = updateDocFields(saved)
        return user, 200

    # get single
    def get(self, id):
        return get(User, id, self)