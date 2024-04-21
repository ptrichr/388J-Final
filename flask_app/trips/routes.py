from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from googlemaps import places

# other imports
from ..forms import NameForm, TimeForm, POIForm
from ..models import Trip, User

# you need to register to create routes, so add flasklogin stuff and force loginrequired
# ok so what routes do we need that are trips related?
# TODO
# 1. a landing page obviously, this should have the name form in the middle
# 2. once we input a name we should go to one of two places - a login, or trip creation route
#   i.   trip creation route - a route that asks for time, and points of interest
#   ii.  this page should update when we add points of interest, it should be some visual list or smth
#   iii. it should also render in a small box below the name of the POI the metro that should be taken to reach that
#       location (so the metro route from A to B)
# 3. we should have something that allows routes to be edited, maybe redirect to the route above

trips = Blueprint("trips", __name__)

@trips.route('/')
def index():
    form = NameForm()
    
    if form.validate_on_submit():
        if current_user.is_authenticated:
            # create trip with that name in mongodb
            # go to trip route
            pass
        
        # otherwise make them login
        return redirect(url_for('users.login'))
        
    render_template('index.html', form=form)
    
