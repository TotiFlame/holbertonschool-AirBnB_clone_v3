#!/usr/bin/python3
"""
Create a new view for Places objects
"""


from flask import Flask, jsonify, abort, request
from models import user, storage
from models.place import Place
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=['GET'], strict_slashes=False)
def show_all_p(city_id):
    place_list = []
    pl = storage.get("City", city_id)
    if pl is None:
        abort(404)
    for places in pl.places:
        place_list.append(places.to_dict())
    return jsonify(place_list)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def show_one_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'], strict_slashes=False)
def delete_one_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def create_place(city_id):
    pl = request.get_json(silent=True)
    if pl is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", pl["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in pl:
        abort(400, 'Missing user_id')
    if "name" not in pl:
        abort(400, 'Missing name')
    
    pl['city_id'] = city_id
    new_place = Place(**pl)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    place_and_id = storage.get(Place, place_id)
    pl = request.get_json(silent=True)

    if place_and_id is None:
        abort(404)
    if pl is None:
        abort(400, 'Not a JSON')
    for key, value in pl.items():
        if key in ['id','user_id', 'city_id' 'created_at', 'updated_at']:
            pass
        setattr(place_and_id, key, value)
    place_and_id.save()
    return jsonify(place_and_id.to_dict()), 200