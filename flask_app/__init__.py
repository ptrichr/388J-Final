# 3p dependencies
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt

# stdlib dependencies
import os

# local dependencies
from client import api

# TODO import api key from somewhere lol could use config file

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
# TODO initialize wmata client

# blueprints
from users.routes import users
from trips.routes import trips

def create_app(test_config=None):
    app = Flask(__name__)
    
    # TODO if config file, populate here
    
    # init clients
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # init blueprints
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(trips, url_prefix='/routes')
    
    login_manager.login_view = "users.login"
    # maybe make a 404
    
    return app