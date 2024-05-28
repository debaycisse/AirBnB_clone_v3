#!/usr/bin/python3
"""The definition for user view. It contains the definition of all supported
HTTP methods to create, retrieve, update, and delete instances of User class
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """retrieves all user instances from the db"""
    if (request.method == 'GET'):
        user_list = []
        for user_obj in storage.all(User).values():
            user_list.append(user_obj.to_dict())
        return jsonify(user_list)


@app_views.route('/users/<string:user_id>', methods=['GET'])
def get_a_user_obj(user_id):
    """retrieves a single User object from the db

    Args:
        user_id - the id of the user object to be retrieved
    """
    user_obj = storage.get(User, user_id)
    if (not user_obj):
        abort(404)
    else:
        user_dict = None
        for k, v in user_obj.items():
            user_dict = v.to_dict()
        return jsonify(user_dict)


@app_views.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user_obj(user_id):
    """deletes a user object whose id is given from the database

    Args:
        user_id - the id attribute of the user object to be deleted
    """
    user_kv_obj = storage.get(User, user_id)
    if (not user_kv_obj):
        abort(404)
    else:
        user_obj = None
        for k, v in user_kv_obj.items():
            user_obj = v
        user_obj.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user_obj():
    """creates an instance of the User class"""
    if (not request.is_json):
        abort(400, message='Not a JSON')
    u_data = request.get_json()
    if ('email' not in u_data):
        abort(400, message='Missing email')
    if ('password' not in u_data):
        abort(400, message='Missing password')
    user_obj = User(**u_data)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'])
def update_user_obj(user_id):
    """updates an instance of the User's object's attribute

    Args:
        user_id - the id attribute of the User object to be updated
    """
    user_kv_obj = storage.get(User, user_id)
    if (not user_kv_obj):
        abort(404)
    if (not request.is_json):
        abort(400, message='Not a JSON')
    u_data = request.get_json()
    user_obj = None
    for k, v in user_kv_obj.items():
        user_obj = v
    for k, v in user_obj.__dict__.items():
        if (('password' in u_data) and (k == 'password')):
            setattr(user_obj, k, u_data['password'])
        if (('first_name' in u_data) and (k == 'first_name')):
            setattr(user_obj, k, u_data['first_name'])
        if (('last_name' in u_data) and (k == 'last_name')):
            setattr(user_obj, k, u_data['last_name'])
    storage.save()
    for k, v in storage.get(User, user_id).items():
        user_obj = v
    return jsonify(user_obj.to_dict()), 200
