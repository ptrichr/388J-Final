from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
from datetime import datetime
import dateutil
from pprint import pprint

# other imports
from ..forms import POIForm, StartForm
from ..models import Trip, User
from .. import client

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
            
            if list(Trip.objects(title=title, author=current_user._get_current_object())):
                flash(message="Cannot have duplicate trip titles")
            else:
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


@trips.route("/plan/<trip_title>", methods=["GET", "POST"])
@login_required
def plan_trip(trip_title):
    form = POIForm()
    trip = Trip.objects(title=trip_title, author=current_user._get_current_object()).first()
    
    if trip is not None:
        pois = list(trip.pois)
        # routes is a list of dictionaries that each contain a key "route" that is mapped
        # to a list of dictionaries (steps) that contain the keys line_info, from, to, which are 
        # dictionaries themselves
        routes = list(trip.routes)
        trip_info = zip(pois, routes)
    else:
        trip_info = []
    
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
                
                if route_info is None:
                    flash(message="There was an error in route computation, please try again")
                else:
                    trip.pois.append({
                                        'name': poi_to_add,
                                        "departure": departure_datetime
                                    })
                    trip.routes.append({'route': route_info})
                    trip.save()
            
            # logic for adding a new poi that is not the first
            else:
                prev = pois[-1]
                route_info = client.compute_route(prev['name'], poi_to_add, prev['departure'])
                
                if route_info is None:
                    flash(message="There was an error in route computation, please try again")
                else:
                    trip.pois.append({
                                        'name': poi_to_add,
                                        "departure": departure_datetime
                                    })
                    trip.routes.append({'route': route_info})
                    trip.save()
            
            # reload
            return redirect(url_for("trips.plan_trip", trip_title=trip.title))
        
    return render_template('trip_planning.html', form=form, info=trip_info)


# remove points of interest
@trips.route('/review/<trip_title>')
@login_required
def remove_poi(trip_title):
    pass