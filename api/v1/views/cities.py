#!/usr/bin/python3
"""
Create a new view for City objects
"""


from flask import Flask, jsonify, abort
from models import state, storage
from models.city import City
from models.state import State
from api.v1.views import app_views

@app_views.route('/states/<state_id>/cities', method=['GET'], strict_slashes=False)
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
