#!/usr/bin/python3
"""This modules houses the definition of the views via Blueprint"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# routes for Blueprint are defined in api/v1/views/index.py
try:
    import api.v1.views.index
except Exception as e:
    pass
