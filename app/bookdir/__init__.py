from flask import Blueprint

from app.bookdir.views import books
from app.bookdir import models

book = Blueprint('books', __name__, url_prefix='/api/v1/books/')

#from app import create_app
#from flask_restful import Api
#app = create_app
#api = Api(app)

from app import app
from flask_restful import Api

api = Api(app)

api.add_resource(books, '/api/v1/books/', '/api/v1/books/<isbn>/')
