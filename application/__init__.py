import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from application.auth import authenticate, identity
from application.database import db
from application.api.user import UserAPI, UsersAPI
from application.config import defaultconfig


def set_api_routes(api):
    api.add_resource(UsersAPI, '/users', endpoint='users')
    api.add_resource(UserAPI, '/user/<int:id>', endpoint='user')


def create_app():
    app = Flask(__name__)
    configobj = os.environ.get('SMARTLUNCH_SETTINGS') or defaultconfig
    app.config.from_object(configobj)
    app.app_context().push()
    with app.app_context():
        db.init_app(app)
        db.create_all()
    api = Api(app)
    set_api_routes(api)
    JWT(app, authenticate, identity)
    return app, db
