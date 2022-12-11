#!/usr/bin/python3
"""
Create a new view for Amenity objects
"""

from flask import Flask, jsonify, abort
from models import state, storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def show_all():
    am_list = []
    ameni = storage.all("Amenity").values()
    if ameni is None:
        abort(404)
    for amenities in ameni:
        am_list.append(amenities.to_dict())
    return jsonify(am_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'], strict_slashes=False)
def show_one(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route("/amenities/<amenity_id>", methods=['DELETE'], strict_slashes=False)
def show_one(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200