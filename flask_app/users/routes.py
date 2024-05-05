from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required, login_user, logout_user
from .. import bcrypt
from random import random
import dateutil

# other imports
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm
from ..models import User, Trip

# TODO
# user route stuff (look at p4)
# 1. need user detail route similar to p4, cept the reviews r replaced by trips
#   i. there should be a button to allow users to retroactively edit trips

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    # if user is already logged in, send to home page
    if current_user.is_authenticated:
        return redirect(url_for("trips.index"))
    
    form = RegistrationForm()
    
    # if form submission details are alright save in db
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        userid = str(round(random() * 10))
        
        # if it's in the database already, generate another one
        while not list(User.objects(userid = userid)):
            userid = str(round(random() * 10))
        
        user = User(username=form.username.data, 
                    userid=userid,
                    password=hashed)
        user.save()
        
        #redirect to login page
        return redirect(url_for("users.login"))
    
    # otherwise re-render page
    return render_template('register.html', title="Register", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    # if user is already logged in, send to home page
    if current_user.is_authenticated:
        return redirect(url_for("trips.index"))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        
        if (user is not None and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user)
            return redirect(url_for("trips.index"))
        else:
            flash(message="Authentication Error. Please Try Logging in Again")
    
    return render_template('login.html', title="Login", form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("trips.index"))

# now displays trips as well
# idk if this url actually works
@users.route('/account', methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    trips = list(Trip.objects(author=current_user))
    
    if request.method == "POST":        
        if update_username_form.submit_username.data and update_username_form.validate():
            # TODO: handle update username form submit
            current_user.modify(username=update_username_form.username.data)
            
        if not update_username_form.errors:
            return redirect(url_for("users.account"))  # redirect to reflect changes
        
    return render_template('account.html', update_username_form=update_username_form, trips=trips)