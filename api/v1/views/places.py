#!/usr/bin/python3
'''
Views for the Place object routes with CRUD methods
'''
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''
    Updates a Place object if it exists
        place_id: ID of the place to update
    Returns a JSON of the updated place
    '''
    request_json = request.get_json()
    if request_json is None:
        abort(400, "Not a JSON")
    put_place = storage.get('Place', place_id)
    if put_place is None:
        abort(404)
    for key, val in request_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(put_city, key, val)
    put_place.save()
    return jsonify(put_place.to_dict()), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''
    Creates a Place object linked to a specific city_id
        city_id: The id of the city to link the new place to
    Returns a JSON of the newly created place otherwise raises 404
    '''
    post_place = request.get_json()
    if not post_place:
        abort(400, "Not a JSON")
    city_to_check = storage.get('City', city_id)
    if city_to_check is None:
        abort(404)
    name = post_place.get("name")
    if name is None:
        abort(400, "Missing name")
    user_id = post_place.get("user_id")
    if user_id is None:
        abort(400, "Missing user_id")
    user_to_check = storage.get('User', user_id)
    if user_to_check is None:
        abort(404)
    new_place = Place()
    new_place.city_id = city_to_check.city_id
    for key, value in post_place.items():
        setattr(new_place, key, value)
    new_city.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''
    Deletes a Place if place_id matches a place in storage
        place_id: place ID of place to be deleted
    Returns an empty JSON
    '''
    place_delete = storage.get('Place', place_id)
    if place_delete is None:
        abort(404)
    storage.delete(place_delete)
    return jsonify({}), 200


@app_views.route('/cites/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place_by_city(state_id):
    '''
    Retrieves json representation of all Place objects by City
    Returns JSON of all Place objects in the City or 404 error if None
    '''
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    place = city.places
    place_list = [places.to_dict() for places in place]
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_places_by_place_id(place_id):
    '''
    Retrieves Place objects by its Place ID
    Returns a JSON of the Place by ID otherwise raises 404
    '''
    place_dict = storage.get('Place', place_id)
    if place_dict is None:
        abort(404)
    return jsonify(place_dict.to_dict())
