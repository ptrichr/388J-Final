# 3p dependencies
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# stdlib dependencies
import os

# local dependencies
from client import api

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
client = api(os.environ.get('GOOG_API_KEY'))

# blueprints
from users.routes import users
from trips.routes import trips

def create_app(test_config=None):
    app = Flask(__name__)
    
    # get config
    app.config.from_pyfile('config.py', silent=False)   
     
    # init clients
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # init blueprints
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(trips, url_prefix='/trips')
    # TODO app.register_error_handler()
    
    login_manager.login_view = 'users.login'
    
    return app