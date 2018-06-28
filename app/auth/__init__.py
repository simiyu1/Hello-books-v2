from flask import Blueprint

auth = Blueprint('authentication', __name__, url_prefix = '/api/v1/auth/')
from app.auth.views import Register,Login, Reset,Logout, RegisterAdmin
from app.user import user

from app import app
from flask_restful import Api

api = Api(app)

api.add_resource(Register, '/api/v1/auth/register')
api.add_resource(Login, '/api/v1/auth/login')
api.add_resource(Reset, '/api/v1/auth/reset')
api.add_resource(Logout, '/api/v1/auth/logout')
#Add an admin user
api.add_resource(RegisterAdmin, '/api/v1/auth/register_admin')
