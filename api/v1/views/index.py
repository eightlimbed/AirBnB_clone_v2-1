#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status')
def status():
    '''
    Retrieves the status of the API
    '''
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    '''
    Returns a dictionary of the models and the number of instances there are.
    '''
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
