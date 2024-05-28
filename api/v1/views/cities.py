#!/usr/bin/python3
"""The definition for state view. It contains the
definition of all supported HTTP methods for state objects"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/states/<string:state_id>/cities', methods=['GET'])
def get_all_cities_state_based(state_id)
    """gets a list of all cities that are based on a given state_id

    Args:
        state_id - the id of the state, where the cities exist
    """
    st_obj = storage.get(State, state_id)
    if (not st_obj):
        abort(404)
    all_cities = storage.all(City)    # {'City.id': <city object>}
    all_state_id_based_cities = []
    for k, v in all_cities.items():
        if (v.state_id == state_id):
            all_state_id_based_cities.append(v.to_dict())
