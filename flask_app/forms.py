from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms_components import TimeField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from models import User

# naming the trip duh
class NameForm(FlaskForm):
    name = StringField(
        "Trip Name", validators=[InputRequired(), Length(min=1, max=50)]
        )
    submit = SubmitField("Let's Go")

# for selecting itinerary start time
class TimeForm(FlaskForm):
    start_time = TimeField("Start Time", validators=[InputRequired()])
    end_time = TimeField("End Time", validators=[InputRequired()])
    submit = SubmitField("Enter")

# for creating routes/adding points
class POIForm(FlaskForm):
    poi = StringField("Enter a Point of Interest", validators=[Length(max=50)])
    submit = SubmitField("Add to Trip")

# do we need email?
class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    # email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    # def validate_email(self, email):
    #     user = User.objects(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError("Email is taken")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=40)])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Submit")

class UpdateUsernameForm(FlaskForm):    
    username = StringField("New Username", validators=[InputRequired(), Length(min=1, max=40)])
    submit_username = SubmitField("Submit") 

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("This username is taken. Pick another username")