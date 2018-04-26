#!/usr/bin/python3
'''
Views for the Place object routes with CRUD methods
'''
from api.v1.views import app_views
from models import storage, classes
from flask import jsonify, abort, request


@app_views.route('/cities/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''
    Updates a place if it exists
    '''
    place = storage.get('place', place_id)
    if place is None:
        abort(404)
    else:
        put_place = request.get_json()
        if not put_place:
            abort(400, "Not a JSON")
        for key, val in put_place.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(place, key, val)
        place.save()
        return jsonify(place.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['POST'], strict_slashes=False)
def create_place(state_id):
    '''
    Creates a place object linked to a specific state ID
        state_id: The id of the state to link the new place to
    Returns a JSON of the newly created place otherwise raises 404
    '''
    post_place = request.get_json()
    if not post_place:
        abort(400, "Not a JSON")
    if 'name' not in post_place:
        abort(400, "Missing name")
    state_to_check = storage.get('State', state_id)
    if state_to_check is None:
        abort(404)
    post_place['state_id'] = state_id
    new_place = classes['place'](**post_place)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''
    Deletes a place if place_id matches a place in storage
        place_id: ID of the place to be deleted
    Returns an empty JSON
    '''
    place_delete = storage.get('Place', place_id)
    if place_delete is None:
        abort(404)
    storage.delete(place_delete)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_place_by_place(city_id):
    '''
    Retrieves json representation of all Place objects by place
    Returns JSON of all Place objects in the place or 404 error if None
    '''
    place = storage.get('City', city_id)
    if place_dict is None:
        abort(404)
    else:
        place_dict = place.places
        place_list = []
        for places in place_dict:
            place_list.append(places)
        return jsonify(place_list)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_places_by_place_id(place_id):
    '''
    Retrieves Place objects by its place ID
    Returns a JSON of the Place otherwise raises 404
    '''
    place_dict = storage.get('Place', place_id)
    if place_dict is None:
        abort(404)
    return jsonify(place_dict.to_dict())
