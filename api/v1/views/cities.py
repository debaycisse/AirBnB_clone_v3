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
def get_all_cities_state_based(state_id):
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
    return jsonify(all_state_id_based_cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'])
def get_city_a_obj(city_id):
    """retrieves a city object whose id is passed

    Args:
        city_id - the id attribute of the city object to be retrieved
    """
    ct_kv_obj = storage.get(City, city_id)
    if (not ct_kv_obj):
        abort(404)
    ct_obj = None
    for k, v in ct_kv_obj.items():
        ct_obj = v.to_dict()
    return jsonify(ct_obj)


@app_views.route('/cities/<string:city_id>', methods=['DELETE'])
def delete_city_obj(city_id):
    """deletes a city instance from the database

    Args:
        city_id - the id attribute of the city object to be deleted
    """
    ct_kv_obj = storage.get(City, city_id)
    if (not ct_kv_obj):
        abort(404)
    ct_obj = None
    for k, v in ct_kv_obj.items():
        ct_obj = v
    ct_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities', methods=['POST'])
def create_city_obj(state_id):
    """creates an instance of City class and stores it in the database

    Args:
        state_id - the attribute of the state where the city is located
    """
    st_kv_obj = storage.get(State, state_id)
    if (not st_kv_obj):
        abort(404)
    if (not request.is_json):
        abort(400, message='Not a JSON')
    data = request.get_json()
    if ('name' not in data):
        abort(400, message='Missing name')
    ct = City(name=data['name'], state_id=state_id)
    ct.save()
    return jsonify(ct.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city_obj(city_id):
    """updates an instance of the City class

    Args:
        city_id - the id attribute of the city instance to be updated
    """
    ct_kv_obj = storage.get(City, city_id)
    if (not ct_kv_obj):
        abort(404)
    if (not request.is_json):
        abort(400, message='Not a JSON')
    data = request.get_json()
    ct_obj = None
    for k, v in ct_kv_obj.items():
        ct_obj = v
    for k, v in ct_obj.__dict__.items():
        if (k == 'name'):
            setattr(ct_obj, k, data['name'])
            storage.save()
    for k, v in storage.get(City, city_id).items():
        return jsonify(v.to_dict()), 200
