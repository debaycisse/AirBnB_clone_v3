#!/usr/bin/python3
"""The definition for the views are done here"""

from flask import jsonify, request
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """returns the status of this rest server"""
    if (request.method == 'GET'):
        return (
                jsonify(
                    {"status": "OK"}
                )
        )
