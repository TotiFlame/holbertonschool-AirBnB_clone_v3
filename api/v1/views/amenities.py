#!/usr/bin/python3
"""
Create a new view for Amenity objects
"""


from flask import Flask, jsonify, abort, request
from models import state, storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def show_all_am():
    am_list = []
    ameni = storage.all("Amenity").values()
    if ameni is None:
        abort(404)
    for amenities in ameni:
        am_list.append(amenities.to_dict())
    return jsonify(am_list)


@app_views.route("/amenities/<amenity_id>",
                 methods=['GET'], strict_slashes=False)
def show_one_am(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_am(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_am():
    amenity = request.get_json(silent=True)
    if amenity is None:
        abort(400, 'Not a JSON')
    if "name" not in amenity:
        abort(400, 'Missing name')
    new_am = Amenity(**amenity)
    new_am.save()
    return jsonify(new_am.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_am(amenity_id):
    amenity_and_id = storage.get(Amenity, amenity_id)
    ameni = request.get_json(silent=True)

    if amenity_and_id is None:
        abort(404)
    if ameni is None:
        abort(400, 'Not a JSON')

    for key, value in ameni.items():
        if key in ['id', 'created_at', 'updated_at']:
            pass
        setattr(amenity_and_id, key, value)
    amenity_and_id.save()
    return jsonify(amenity_and_id.to_dict()), 200
