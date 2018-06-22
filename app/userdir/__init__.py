from flask import Flask
from flask import Blueprint

user = Blueprint('users', __name__, url_prefix='/api/v1/users/')

from app.userdir.views import Users, Borrow, Return
from app.userdir import models

from app import app
from flask_restful import Api

api = Api(app)

api.add_resource(Users, '/api/v1/users/', '/api/v1/users/<int:userid>/')
api.add_resource(Borrow, '/api/v1/users/books/<book_id>')
api.add_resource(Return, '/api/v1/users/books/<book_id>')
