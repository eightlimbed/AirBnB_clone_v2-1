#!/usr/bin/python3
"""
Creates GET, POST, DELETE, & PUT requests for State objects
"""
from api.v1.views import app_views
from flask import Blueprint, jsonify, abort, request, make_response
from models import storage
import json
from models.state import State


app_views.url_map.strict_slashes = False


@app_views.route('/states', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """
    Gets a State object based on given state id
        state_id: ID of the state to get.
    Returns a JSON of the state
    """
    if state_id is None:
        states = storage.all('State')
        states_list = [object.to_dict() for key, object in states.items()]
        return jsonify(states_list)
    states = storage.get('State', state_id)
    if states_list is not None:
        return jsonify(states.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a State object based on a given state id
        state_id: ID of the state to delete
    Returns an empty JSON and HTTP status code 200 if successful
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def post_state():
    """
    Creates a State object
    Returns a JSON of the new State along with HTTP status code 201
    """
    given_json = request.get_json()
    if given_json is None:
        abort(make_response("Not a JSON", 404))
    if given_json.get('name') is None:
        abort(make_response("Missing name", 400))
    new_state = State(**given_json)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """
    Updates a State object based on a given state id
        state_id: ID of the state to be updated
    Returns the updated State object with the HTTP status code 200
    """
    given_json = request.get_json()
    if given_json is None:
        abort(make_response("Not a JSON", 400))
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    to_ignore = ['id', 'created_at', 'updated_at']
    for key, value in given_json.items():
        if key not in to_ignore:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
