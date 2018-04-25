#!/usr/bin/python3

'''
RESTful API for hbnb
'''
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    '''
    404 error handler
    '''
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def close_db(error):
    '''
    Closes the storage engine at teardown
    '''
    storage.close()


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST')
    if host is None:
        host = '0.0.0.0'
    port = os.getenv('HBNB_API_PORT')
    if port is None:
        port = 5000
    app.run(host, int(port))
