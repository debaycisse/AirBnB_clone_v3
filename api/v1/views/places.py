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


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_place_obj(place_id):
    """retrieves an instqnce of the Place model

    Args:
        place_id - id attribute of a place instance to be retrieved
    """
    pl_kv_obj = storage.get(Place, place_id)
    if (not pl_kv_obj):
        abort(404)
    pl_obj = None
    for k, v in pl_kv_obj.items():
        pl_obj
    return jsonify(pl_obj.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_place_obj(place_id):
    """deletes a Place modle instance from the db

    Args:
        place_id - the id attribite of the instance to be deleted
    """
    pl_kv_obj = storage.get(Place, place_id)
    if (not pl_kv_obj):
        abort(404)
    pl_obj = None
    for k, v in pl_kv_obj.items():
        pl_obj = v
    pl_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place_obj(city_id):
    """creates an instance of the Place model, stores, and returns it

    Args:
        city_id - the id attribute of the city where this instance will exist
    """
    ct_kv_obj = storage.get(City, city_id)
    if (not ct_kv_obj):
        abort(404)
    if (not request.is_json):
        abort(400, message='Not a JSON')
    data = request.get_json()
    if ('user_id' not in data):
        abort(400, message='Missing user_id')
    user_id = data['user_id']
    user_kv_obj = storage.get(User, user_id)
    if (not user_kv_obj):
        abort(404)
    user_obj = None
    for k, v in user_kv_obj.items():
        user_obj = v
    if ('name' not in user_obj):
        abort(400, message='Missing name')
    pl_obj = Place(**data)
    return jsonify(pl_obj.to_dict()), 201


@app_views.route('places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place_obj(place_id):
    """updates or modifies an existing Place model instance

    Args:
        place_id - the id attribute of the instance to be modified
    """
    pl_kv_obj = storage.get(Place, place_id)
    if (not pl_kv_obj):
        abort(404)
    if (not request.is_json):
        abort(400, message='Not a JSON')
    data = request.get_json()
    pl_obj = None
    for k, v in pl_kv_obj.items():
        pl_obj = v
    for k, v in pl_obj.__dict__.items():
        nid = (k != 'id')
        nid2 = (k != 'user_id')
        ncid = (k != 'city_id')
        ncat = (k != 'created_at')
        nuat = (k != 'updated_at')
        k_ = (k in data)
        if (nid and nid2 and ncid and ncat and nuat and k_):
            setattr(pl_obj, k, data[k])
    storage.save()
    for k, v in storage.get(Place, place_id).items():
        pl_obj = v
    return jsonify(pl_obj.to_dict()), 200
