#!/usr/bin/python3
"""The definition for amenity view. It contains the definition of all
required HTTP methods for state objects to ensure that one can create, get,
update, and delete an instance of Amenity class"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """retrieves a list of all instances of Amenity class"""
    am_list = []
    for am_obj in storage.all(Amenity).values():
        am_list.append(am_obj.to_dict())
    return jsonify(am_list)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_an_instance(amenity_id):
    """retrieves an instance of the Amenity class

    Args:
        amenity_id - the id attribute of the instance to be retrieved
    """
    am_obj = storage.get(Amenity, amenity_id)
    if (not am_obj):
        abort(404)
    else:
        am_dict = None
        for k, v in am_obj.items():
            am_dict = v.to_dict()
        return jsonify(am_dict)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an instance of Amenity class whose
    id matches with the given one

    Args:
        amenity_id - the id of the instance to be dleeted
    """
    am_kv_obj = storage.get(Amenity, amenity_id)
    if (not am_kv_obj):
        abort(404)
    am_obj = None
    for k, v in am_kv_obj.items():
        am_obj = v
    am_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity_obj():
    """creates an instance of the Amenity class"""
    if (not request.is_json):
        abort(400, message='Not a JSON')
    data = request.get_json()
    if ('name' not in data):
        abort(400, message='Missing name')
    am = Amenity(**data)
    am.save()
    return jsonify(am.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates an instance of Amenity class whose id attribute is passed

    Args:
        amenity_id - the attribute of the instance to be updated
    """
    am_kv_obj = storage.get(Amenity, amenity_id)
    if (not am_kv_obj):
        abort(404)
    if (not request.is_json):
        abort(400, message='Not a JSON')
    data = request.get_json()
    am_obj = None
    for k, v in am_kv_obj.items():
        am_obj = v
    for k, v in am_obj.__dict__.items():
        if (k == 'name'):
            setattr(am_obj, k, data['name'])
            storage.save()
    for k, v in storage.get(Amenity, amenity_id).items():
        am_obj = v
    return jsonify(am_obj.to_dict()), 200
