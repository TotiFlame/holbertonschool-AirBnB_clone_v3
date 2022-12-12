#!/usr/bin/python3
"""
Create a new view for reviews objects
"""


from flask import Flask, jsonify, abort, request
from models import state, storage
from models.review import Review
from models.place import Place
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews",
                 methods=['GET'], strict_slashes=False)
def show_all_reviews(place_id):
    review_list = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for p in place.review:
        review_list.append(p.to_dict())
    return jsonify(review_list)


@app_views.route("/reviews/<review_id>",
                 methods=['GET'], strict_slashes=False)
def show_review(review_id):
    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)
    return jsonify(rev.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=['DELETE'], strict_slashes=False)
def del_(review_id):
    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)
    storage.delete(rev)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_ct(place_id):
    pl = storage.get(Place, place_id)
    if pl is None:
        abort(404)
    rev = request.get_json(silent=True)
    if rev is None:
        abort(400, 'Not a JSON')
    if "user_id" not in rev:
        abort(400, 'Missing user_id')
    rev['place_id'] = place_id
    new_rev = Review(**rev)
    new_rev.save()
    return jsonify(new_rev.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_ct(review_id):
    rev_and_id = storage.get(Review, review_id)
    rev = request.get_json(silent=True)

    if rev_and_id is None:
        abort(404)
    if rev is None:
        abort(400, 'Not a JSON')

    for key, value in rev.items():
        if key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            pass
        setattr(rev_and_id, key, value)
    rev_and_id.save()
    return jsonify(rev_and_id.to_dict()), 200
