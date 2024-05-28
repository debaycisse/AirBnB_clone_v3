#!/usr/bin/python3
"""This modules defines (Blueprint) view for Review model
instances to handle all default RESTFul API actions"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_places_based_review_obj(place_id):
    """retrieves a list of review instances of a given place

    Args:
        place_id - the id attribute of the place instance
        whose reviews are to be retrieved
    """
    pl_kv_obj = storage.get(Place, place_id)
    if (not pl_kv_obj):
        abort(404)
    pl_based_rv_list = []
    for k, v in storage.all(Review).items():
        if (v['place_id'] == place_id):
            pl_based_rv_list.append(v.to_dict())
    return jsonify(pl_based_rv_list)


@app_views.route('/reviews/<string:review_id>', methods=['GET'])
def get_a_review(review_id):
    """retrieves a single instance of the Review model

    Args:
        review_id - the id attribute of the instance to be retrieved
    """
    rv_kv_obj = storage.get(Review, review_id)
    if (not rv_kv_obj):
        abort(404)
    for k, v in rv_kv_obj.items():
        return jsonify(v.to_dict())


@app_reviews.route('/reviews/<string:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """deletes an instance of the Review model whose id is passed

    Args:
        review_id - the id attribute of the instance to be deleted
    """
    rv_kv_obj = storage.get(Review, review_id)
    if (not rv_kv_obj):
        abort(404)
    rv_obj = None
    for k, v in rv_kv_obj.items():
        rv_obj = v
    rv_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_a_review(place_id):
    """creates an instance of the Review model, stores, and returns it

    Args:
        place_id - the id attribute of the Place model instance on
        which the new review applies
    """
    pl_kv_obj = storage.get(Place, place_id)
    if (not pl_kv_obj):
        abort(404)
    if (not request.is_json):
        abort(400, message='Not a JSON')
    data = request.get_json()
    if ('user_id' not in data):
        abort(400, message='Missing user_id')
    user_kv_obj = storage.get(User, data['user_id'])
    if (not user_kv_obj):
        abort(404)
    if ('text' not in data):
        abort(400, message='Missing text')
    rv_obj = Review(**data)
    rv_obj.save()
    return jsonify(rv_obj.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['PUT'])
def update_review(review_id):
    """updates or modifies an existing instance of a Review model

    Args:
        review_id - the id attribute of the instance to be modified
    """
    rv_kv_obj = storage.get(Review, review_id)
    if (not rv_kv_obj):
        abort(404)
    if (not request.is_json):
        abort(400, message='Not a JSON')
    data = request.get_json()
    for k, v in rv_kv_obj.items():
        if (k == 'text' and 'text' in data):
            setattr(v, k, data['text'])
            storage.save()
    for k, v in storage.get(Review, review_id).items():
        return jsonify(v.to_dict()), 200
