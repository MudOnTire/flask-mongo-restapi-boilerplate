from flask import Flask
from flask_compress import Compress
from flask_restful import Api
from flask_cors import CORS
from mongoengine import connect
from src.api.auth import SignInApi, SignUpApi
from src.api.user import UsersApi, UserApi
from src.api.post import PostsApi, PostApi
from src.api.comment import CommentsApi

app = Flask(__name__)
# cors
CORS(app, origins=['*'], supports_credentials=True)
# compress response
Compress(app)
# connect mongodb
connection = connect('restful_app', host='localhost', port=27017)

api = Api(app)

api.add_resource(SignInApi, '/api/signin')
api.add_resource(SignUpApi, '/api/signup')
api.add_resource(UsersApi, '/api/users')
api.add_resource(UserApi, '/api/users/<string:id>')
api.add_resource(PostsApi, '/api/posts')
api.add_resource(PostApi, '/api/posts/<string:id>')
api.add_resource(CommentsApi, '/api/comments')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
