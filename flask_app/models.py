from flask_login import UserMixin
from . import db, login_manager
import dateutil

# maybe change later if issues arise
@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(min_length=1, 
                              max_length=40, 
                              unique=True, 
                              required=True)
    userid = db.StringField(required=True)
    password = db.StringField(required=True)

    # Returns unique string identifying our object
    def get_id(self):
        return self.userid
    
class Trip(db.Document):
    # maybe add like a time spent field as a visual? idk
    author = db.StringField(required=True)
    title = db.StringField(required=True)
    start_time = db.DateTimeField(required=True)
    pois = db.ListField(db.DictField(), default=[])
    routes = db.ListField(db.DictField(), default=[])
    