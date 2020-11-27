from datetime import datetime
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash, generate_password_hash
from src.common.utils import updateDocFields, createToken

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

# register
register_args = reqparse.RequestParser()
register_args.add_argument("name",
                       type=str,
                       help="Username is required",
                       required=True)
register_args.add_argument("password",
                       type=str,
                       help="Password is required",
                       required=True)
register_args.add_argument("role", type=str, default="user")



class SignInApi(Resource):
    def post(self):
        args = login_args.parse_args()
        name = args['name']
        password = args['password']
        db_user = User.objects(name=name).first()
        if db_user is None:
            return 404
        passed = check_password_hash(db_user['password'], password)
        if passed:
            user = updateDocFields(db_user)
            token = createToken(user['id'])
            return user, 200, {'Set-Cookie': f'token={token}'}
        return 400

class SignUpApi(Resource):
    def post(self):
        args = register_args.parse_args()
        hashed_pass = generate_password_hash(args['password'])
        new_user = User(name=args['name'],
                        password=hashed_pass,
                        role=args['role'])
        saved = new_user.save()
        user = updateDocFields(saved)
        return user, 201