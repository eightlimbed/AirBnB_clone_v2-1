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
from models.review import Review
from flask import jsonify, abort, request


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''
    Updates a Review object if it exists
        review_id: ID of the review to update
    Returns a JSON of the updated review
    '''
    request_json = request.get_json()
    if request_json is None:
        abort(400, "Not a JSON")
    put_review = storage.get('Review', review_id)
    if put_review is None:
        abort(404)
    for key, val in request_json.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'place_id']:
            setattr(put_review, key, val)
    put_review.save()
    return jsonify(put_review.to_dict()), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''
    Creates a Review object linked to a specific place_id
        place_id: The id of the place to link the new Review to
    Returns a JSON of the newly created Review otherwise raises 404
    '''
    post_review = request.get_json()
    if post_review is None:
        abort(400, "Not a JSON")
    place_to_check = storage.get('Place', place_id)
    if place_to_check is None:
        abort(404)
    user_id = post_review.get("user_id")
    if user_id is None:
        abort(400, "Missing user_id")
    user_to_check = storage.get('User', user_id)
    if user_to_check is None:
        abort(404)
    text = post_place.get("text")
    if text is None:
        abort(400, "Missing text")
    new_review = Review()
    new_review.place_id = place_id
    for key, value in post_review.items():
        setattr(new_review, key, value)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''
    Deletes a Review object if review_id matches a review in storage
        review_id: ID of the review to be deleted
    Returns an empty JSON
    '''
    review_delete = storage.get('Review', review_id)
    if review_delete is None:
        abort(404)
    storage.delete(review_delete)
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_by_place(place_id):
    '''
    Retrieves json representation of all Review objects by place
    Returns JSON of all Review objects in the City or 404 error if None
    '''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    review_list = place.reviews
    review_list = [reviews.to_dict() for reviews in review_list]
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_review_id(review_id):
    '''
    Retrieves Review objects by its ID
    Returns a JSON of the Review object otherwise raises 404
    '''
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200
