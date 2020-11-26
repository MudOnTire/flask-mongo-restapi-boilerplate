from datetime import datetime
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from src.common.utils import updateDocFields

from src.models.user import User

# login
login_args = reqparse.RequestParser()
login_args.add_argument("name",
                        type=str,
                        help="Username is required",
                        required=True)
login_args.add_argument("password",
                        type=str,
                        help="Password is required",
                        required=True)
login_args.add_argument("role", type=str, default="user")

class LoginApi(Resource):
    def post(self):
        args = login_args.parse_args()
        name = args['name']
        password = args['password']
        user = User.objects(name=name).first()
        if user is None:
            return 404
        passed = check_password_hash(user['password'], password)
        if passed:
            return updateDocFields(user), 200
        return 400