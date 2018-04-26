#!/usr/bin/python3
'''
Views for the /cities and /cities/<city_id> routes with CRUD methods
'''
from api.v1.views import app_views
from models import storage, classes
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''
    Updates a city if it exists
    '''
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    else:
        put_city = request.get_json()
        if not put_city:
            abort(400, "Not a JSON")
        for key, val in put_city.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, val)
        city.save()
        return jsonify(city.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    '''
    Creates a City object linked to a specific state ID
        state_id: The id of the state to link the new city to
    Returns a JSON of the newly created city otherwise raises 404
    '''
    post_city = request.get_json()
    if not post_city:
        abort(400, "Not a JSON")
    if 'name' not in post_city:
        abort(400, "Missing name")
    state_to_check = storage.get('State', state_id)
    if state_to_check is None:
        abort(404)
    post_city['state_id'] = state_id
    new_city = classes['City'](**post_city)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    '''
    Deletes a city if city_id matches a city in storage
        city_id: 
    '''
    city_delete = storage.get('City', city_id)
    if city_delete is None:
        abort(404)
    storage.delete(city_delete)
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_city_by_state(state_id):
    '''
    Retrieves json representation of all City objects by State
    Returns JSON of all City objects in the state or 404 error if None
    '''
    city_dict = storage.get('State', state_id)
    if city is None:
        abort(404)
    else:
        city_dict = city.cities
        city_list = []
        for cities in city_dict:
            city_list.append(cities)
        return jsonify(city_list)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_cities_by_city_id(city_id):
    '''
    Retrieves City objects by city ID
    Returns a JSON of the City by ID otherwise raises 404
    '''
    city_dict = storage.get('City', city_id)
    if city_dict is None:
        abort(404)
    return jsonify(city_dict.to_dict())
