#!/usr/bin/python3
"""Module that defines a flask application whose views have been seperated"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
host_ip = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def close_db(error):
    """closes the database connection after each request

    Args:
        error - a returned error from any given request
    """

    storage.close()


app.register_blueprint(app_views)


if __name__ == '__main__':
    app.run(host=host_ip, port=port, threaded=True)
