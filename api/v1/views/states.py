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


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """retrieves all state instances from the db"""
    if (request.method == 'GET'):
        st_list = []
        for st_obj in storage.all(State).values():
            st_list.append(st_obj.to_dict())
        return jsonify(st_list)


@app_views.route('/states/<string:state_id>', methods=['GET'])
def get_a_state_obj(state_id):
    """retrieves a single state object from the db

    Args:
        state_id - the id of the state object to be retrieved
    """
    st_obj = storage.get(State, state_id)
    if (not st_obj):
        abort(404)
    else:
        st_dict = None
        for k, v in st_obj.items():
            st_dict = v.to_dict()
        return jsonify(st_dict)


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_state(state_id):
    """deletes a state object whose id is given from the database

    Args:
        state_id - the id attribute of the state object to be deleted
    """
    st_kv_obj = storage.get(State, state_id)
    if (not st_kv_obj):
        abort(404)
    else:
        st_obj = None
        for k, v in st_kv_obj.items():
            st_obj = v
        st_obj.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state_obj():
    """creates an instance of the state class"""
    if (not request.is_json):
        abort(400, message='Not a JSON')
    u_data = request.get_json()
    if ('name' not in u_data):
        abort(400, message='Missing name')
    st = State(**u_data)
    st.save()
    return jsonify(st.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def update_state(state_id):
    """updates a state object attribute

    Args:
        state_id - the id attribute of the state object to be updated
    """
    st_kv_obj = storage.get(State, state_id)
    if (not st_kv_obj):
        abort(404)
    if (not request.is_json):
        abort(400, message='Not a JSON')
    u_data = request.get_json()
    st_obj = None
    for k, v in st_kv_obj.items():
        st_obj = v
    for k, v in st_obj.__dict__.items():
        if (k == 'name'):
            setattr(st_obj, k, u_data['name'])
            storage.save()
    for k, v in storage.get(State, state_id).items():
        st_obj = v
    return jsonify(st_obj.to_dict()), 200
