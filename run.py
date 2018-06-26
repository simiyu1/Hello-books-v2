import os
from flask import Flask
# Blueprint names
from app.book import book
from app.user import user
from app.auth import auth

from app import app

# Register the blueprints
app.register_blueprint(book)
app.register_blueprint(user)
app.register_blueprint(auth)
#adding the config


if __name__ == '__main__':
    app.run(debug =True, port=5000)