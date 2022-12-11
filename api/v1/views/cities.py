#!/usr/bin/python3
"""
Create a new view for City objects
"""


from flask import Flask, jsonify, abort
from models import state, storage
from api.v1.views import app_views

@app_views.route('/states/<state_id>/cities', method=['GET'], strict_slashes=False)
def show_all_cities(state_id):
    """
    It returns a JSON
    representation of all the cities in a state
    """
    states =  storage.all("State").values()
    for state in states:
        if state.id == state_id:
            return jsonify(state.cities.to_dict())
    abort(404)
