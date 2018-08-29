import os
from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.url_map.strict_slashes = False
# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'This Method is not allowed'}), 405)

@app.errorhandler(404)
def not_found2(error):
    return make_response(jsonify({'error': 'This URL is broken, please check and try again '}), 404)
  
