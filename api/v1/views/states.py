#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    '''
    Deletes a state if state_id matches a state in storage
    '''
    for key, obj in storage.all('State').items():
        if obj.id == state_id:
            storage.delete(obj)
            return jsonify({})
    abort(404)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    '''
    Retrieves json representation of a state if it exists
    '''
    for key, obj in storage.all('State').items():
        if obj.id == state_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def show_states():
    '''
    Retrieves the list of all State objects
    '''
    states = {}
    for key, obj in storage.all('State').items():
        states[key] = obj.to_dict()
    return jsonify(states)

