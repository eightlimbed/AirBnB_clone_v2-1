#!/usr/bin/python3
'''
Views for the /amenities CRUD methods
'''
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''
    Updates a amenity if it exists
    '''
    if not request.is_json:
        abort(400, "Not a JSON")
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    new_amenity = request.get_json()
    for key, val in new_amenity.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, val)
    storage.save()
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''
    Creates a amenity if amenity_id matches a amenity in storage
    '''
    if not request.is_json:
        abort(400, "Not a JSON")
    amenity_json = request.get_json()
    if 'name' not in amenity_json.keys():
        abort(400, "Missing name")
    new_amenity = Amenity()
    storage.new(new_amenity)
    for key, val in amenity_json.items():
        new_amenity.__dict__[key] = val
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    '''
    Deletes a amenity if amenity_id matches a amenity in storage
    '''
    for key, obj in storage.all('Amenity').items():
        if obj.id == amenity_id:
            storage.delete(obj)
            return jsonify({})
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    '''
    Retrieves json representation of a amenity if it exists
    '''
    for key, obj in storage.all('Amenity').items():
        if obj.id == amenity_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def show_amenities():
    '''
    Retrieves the list of all Amenity objects
    '''
    amenities = []
    for key, obj in storage.all('Amenity').items():
        amenities.append(obj.to_dict())
    return jsonify(amenities)
