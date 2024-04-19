from flask import Blueprint, render_template, url_for, request, redirect
# other imports

# you need to register to create routes, so add flasklogin stuff and force loginrequired
# ok so what routes do we need that are trips related?
# TODO
# 1. a landing page obviously, this should have the name form in the middle
# 2. once we input a name we should go to a route that asks for time, and points of interest
#   i. this page should update when we add points of interest, it should be some visual list or smth
#   ii. it should also render in a small box below the name of the POI the metro that should be taken to reach that
#       location (so the metro route from A to B)
# 3. we should have something that allows routes to be edited, maybe redirect to the route above

trips = Blueprint("trips", __name__)