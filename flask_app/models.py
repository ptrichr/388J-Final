from flask_login import UserMixin
from . import db, login_manager

# maybe change later if issues arise
@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(min_length=1, 
                              max_length=40, 
                              unique=True, 
                              required=True)
    # email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()

    # Returns unique string identifying our object
    def get_id(self):
        # TODO: implement
        return self.username
    
class Trip(db.Document):
    start_time = db.StringField(required=True)
    end_time = db.StringField(required=True)
    pois = db.ListField(db.StringField(), required=True)
    # routes = idk what this should be
    