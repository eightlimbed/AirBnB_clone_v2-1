#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status')
def status():
    return jsonify({'status': 'OK'})

@app_views.route('/stats')
def stats():
    stats = {
        'amenities': storage.count('Amenity')
    }
    return jsonify({'stats': stats})
