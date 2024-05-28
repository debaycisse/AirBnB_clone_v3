#!/usr/bin/python3
"""This modules houses the definition of the views via Blueprint"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

try:
    import api.v1.views.index
    import api.v1.views.states
    import api.v1.views.cities
    import api.v1.views.amenities
    import api.v1.views.users
    import api.v1.views.places
    import api.v1.views.places_reviews
except ImportError:
    pass
"""# routes for Blueprint are defined in api/v1/views/index.py
try:
    from api.v1.views import index, states
except Exception as e:
    pass"""
