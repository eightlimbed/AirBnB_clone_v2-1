#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    '''
    Retrieves the list of all State objects
    '''
    states = {}
    for key, obj in storage.all('State').items():
        states[key] = obj.to_dict()
    return jsonify(states)
