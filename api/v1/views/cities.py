#!/usr/bin/python3
"""
Create a new view for City objects
"""


from flask import Flask, jsonify, abort, request
from models import state, storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities",
                 methods=['GET'], strict_slashes=False)
def show_all_cities(state_id):
    """
    It returns a JSON
    representation of all the cities in a state
    """
    cities_list = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def show_city(city_id):
    """
    It gets a city from the database, and if it
    doesn't exist, it returns a 404 error
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """
    It deletes a city from the database
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_ct(state_id):
    """
    - Creates a State
    - If the HTTP body request is not valid JSON,
    raise a 400 error with the message Not a JSON
    - If the dictionary doesn’t contain the key name,
    raise a 400 error with the message Missing name
    """
    st = storage.get(State, state_id)
    if st is None:
        abort(404)
    city = request.get_json(silent=True)
    if city is None:
        abort(400, 'Not a JSON')
    if "name" not in city:
        abort(400, 'Missing name')
    city['state_id'] = state_id
    new_ct = City(**city)
    new_ct.save()
    return jsonify(new_ct.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_ct(city_id):
    city_and_id = storage.get(City, city_id)
    city = request.get_json(silent=True)

    if city_and_id is None:
        abort(404)
    if city is None:
        abort(400, 'Not a JSON')

    for key, value in city.items():
        if key in ['id', 'created_at', 'updated_at']:
            pass
        setattr(city_and_id, key, value)
    city_and_id.save()
    return jsonify(city_and_id.to_dict()), 200
