from datetime import datetime
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from src.common.utils import updateDocFields

from src.models.user import User
from src.api.base import query, delete, get, AuthResource

# put
put_args = reqparse.RequestParser()
put_args.add_argument("name", type=str)
put_args.add_argument("password", type=str)
put_args.add_argument("role", type=str)

class UsersApi(AuthResource):
    # query
    def get(self):
        return query(User, self)

    # delete
    def delete(self):
        return delete(User, self)


class UserApi(AuthResource):
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
    def get(self, user, id):
        return get(User, id, self)