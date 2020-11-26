from flask import Flask
from flask_compress import Compress
from flask_restful import Api
from flask_cors import CORS
from mongoengine import connect
from src.api.user import UsersApi

app = Flask(__name__)
# cors
CORS(app, origins=['*'], supports_credentials=True)
# compress response
Compress(app)
# connect mongodb
connection = connect('restful_app', host='localhost', port=27017)

api = Api(app)

api.add_resource(UsersApi, '/api/users')

if __name__ == "__main__":
    app.run(debug=False, port=5000)
