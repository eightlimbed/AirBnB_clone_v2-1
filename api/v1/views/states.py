#!/usr/bin/python3
'''
Views for the /states and /states/<state_id> routes with CRUD methods
'''
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''
    Updates a state if it exists
    '''
    if not request.json:
        abort(400, "Not a JSON")
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    new_state = request.get_json()
    for key, val in new_state.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, val)
    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''
    Creates a state if state_id matches a state in storage
    '''
    if not request.json:
        abort(400, "Not a JSON")
    state_json = request.get_json()
    if 'name' not in state_json.keys():
        abort(400, "Missing name")
    new_state = State()
    storage.new(new_state)
    for key, val in state_json.items():
        new_state.__dict__[key] = val
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
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
