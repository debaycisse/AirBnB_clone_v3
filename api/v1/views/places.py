#!/usr/bin/python3
"""This module contains the definition of the HTTP methods to create, modify,
retrieve, and delete instances of the Place model"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places_in_city(city_id):
    """retrieves all place instances that are linked to a passed city's id

    Args:
        city_id - the id attribute of the city where the
        place instances must belong
    """
    city_obj_kv = storage.get(City, city_id)
    if (not city_obj_kv):
        abort(404)
    pl_list = []
    for k, pl_obj in storage.all(Place).items():
        if (pl_obj['city_id'] == city_id):
            pl_list.append(pl_obj.to_dict())
    return jsonify(pl_list)
