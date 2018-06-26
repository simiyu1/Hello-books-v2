from flask import Flask
from flask import Blueprint

user = Blueprint('users', __name__, url_prefix='/api/v1/users/')

from app.user.views import Users, Borrow, Return
from app.user import models

from app import app
from flask_restful import Api

api = Api(app)

api.add_resource(Users, '/api/v1/users/', '/api/v1/users/<int:userid>/')
api.add_resource(Borrow, '/api/v1/users/books/<int:bookid>')
api.add_resource(Return, '/api/v1/users/books/<int:bookid>')
