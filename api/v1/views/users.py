#!/usr/bin/python3
'''
Views for the /users and /users/<user_id> routes with CRUD methods
'''
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''
    Updates a user if it exists
    '''
    if not request.is_json:
        abort(400, "Not a JSON")
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    new_user = request.get_json()
    for key, val in new_user.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, val)
    storage.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''
    Creates a user if user_id matches a user in storage
    '''
    if not request.is_json:
        abort(400, "Not a JSON")
    user_json = request.get_json()
    if 'email' not in user_json.keys():
        abort(400, "Missing email")
    if 'password' not in user_json.keys():
        abort(400, "Missing password")
    new_user = User()
    storage.new(new_user)
    for key, val in user_json.items():
        new_user.__dict__[key] = val
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    '''
    Deletes a user if user_id matches a user in storage
    '''
    for key, obj in storage.all('User').items():
        if obj.id == user_id:
            storage.delete(obj)
            return jsonify({})
    abort(404)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    '''
    Retrieves json representation of a user if it exists
    '''
    for key, obj in storage.all('User').items():
        if obj.id == user_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def show_users():
    '''
    Retrieves the list of all User objects
    '''
    users = []
    for key, obj in storage.all('User').items():
        users.append(obj.to_dict())
    return jsonify(users)
