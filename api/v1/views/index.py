#!/usr/bin/python3
"""The definition for the views are done here"""

from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """returns the status of this rest server"""
    if (request.method == 'GET'):
        return (
                jsonify(
                    {"status": "OK"}
                )
        )


@app_views.route('/stats', methods=['GET'])
def stats():
    """retrieves the number of each objects by type"""
    if (request.method == 'GET'):
        amenity_count = storage.count(Amenity)
        city_count = storage.count(City)
        place_count = storage.count(Place)
        review_count = storage.count(Review)
        state_count = storage.count(State)
        user_count = storage.count(User)
        return (
                jsonify(
                    {"amenities": amenity_count, "cities": city_count,
                     "places": place_count, "reviews": review_count,
                     "states": state_count, "users": user_count}
                )
        )
