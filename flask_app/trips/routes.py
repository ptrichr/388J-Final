from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from datetime import datetime
import dateutil
from pprint import pprint

# other imports
from ..forms import POIForm, StartForm
from ..models import Trip, User
from .. import client

# you need to register to create routes, so add flasklogin stuff and force loginrequired
# ok so what routes do we need that are trips related?
# TODO
# 1. a landing page obviously, this should have the name form in the middle
# 2. once we input a name we should go to one of two places - a login, or trip creation route
#   i.   trip creation route - a route that asks for time, and points of interest
#   ii.  this page should update when we add points of interest, it should be some visual list or smth
#   iii. it should also render in a small box below the name of the POI the metro that should be taken to reach that
#        location (so the metro route from A to B)
#   iv. there should be a button on the bottom of the page that says finish and just redirects to the account page
#       ^^ this can probably be html thing, since trip is saved after each poi added

# ok maybe we should change the structure:
# index page is just an input field that takes a location in DC and a time to leave
# the first poi is that location in DC, and has a start time filled in by the arrival time at the station
# then user has to fill in the end time, and from there we do the rest of the POIs

trips = Blueprint("trips", __name__)

@trips.route("/", methods=["GET", "POST"])
def index():
    form = StartForm()
        
    if request.method == "POST":
        if current_user.is_authenticated == False:
            return redirect(url_for("users.login"))
        
        if form.validate_on_submit():          
            # just get the start location and make that the placeholder title
            title = form.title.data
            depart_cp = form.depart_cp.data
            
            # initialize in DB
            trip = Trip(author=current_user._get_current_object(),
                        title=title,
                        start_time=depart_cp,
                        pois=[],
                        routes=[])
            trip.save()
                        
            # redirect to init route
            return redirect(url_for("trips.plan_trip", trip_title=title))
        
    # maybe add title field
    return render_template('index.html', form=form)


# TODO something is going wrong here with the time
@trips.route("/plan/<trip_title>", methods=["GET", "POST"])
@login_required
def plan_trip(trip_title):    
    form = POIForm()
    trip = Trip.objects(title=trip_title).first()
    pois = list(trip.pois)
    # routes is a list of dictionaries that each contain a key "route" that is mapped
    # to a list of dictionaries (steps) that contain the keys line_info, from, to, which are 
    # dictionaries themselves
    routes = list(trip.routes)
    trip_info = zip(pois, routes)
    
    if request.method == "POST":
        
        if form.validate_on_submit():
            poi_to_add = form.poi.data
            leave_poi_t = form.depart.data
            depart_cp = trip.start_time
            
            # formatting time as datetime object
            departure_datetime = datetime(depart_cp.year,
                                          depart_cp.month,
                                          depart_cp.day,
                                          leave_poi_t.hour,
                                          leave_poi_t.minute)
            
            # logic for if we need to compute route from college park (adding first POI)
            if not pois:
                route_info = client.compute_route("University of Maryland, College Park", 
                                                  poi_to_add, 
                                                  depart_cp)
                trip.pois.append({
                                    'name': poi_to_add,
                                    "departure": departure_datetime
                                })
                trip.routes.append({'steps': route_info})
                trip.save()
            
            # logic for adding a new poi that is not the first
            else:
                prev = pois[-1]
                route_info = client.compute_route(prev['name'], poi_to_add, prev['departure'])
                trip.pois.append({
                                    'name': poi_to_add,
                                    "departure": departure_datetime
                                })
                trip.routes.append({'route': route_info})
                pprint(route_info)
                trip.save()
            
            # reload
            return redirect(url_for("trips.plan_trip", trip_title=trip.title))
        print(form.errors)
    return render_template('trip_planning.html', form=form, info=trip_info)


# review will handle the route calculation back to college park
@trips.route('/review/<trip_title>')
@login_required
def review_trip(trip_title):
    pass