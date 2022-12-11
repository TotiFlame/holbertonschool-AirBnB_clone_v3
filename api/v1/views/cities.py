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
    cities_list = []
    cities = storage.all("City").values()
    
    for st in storage.all("State").values():
        if st.id == state_id:
            state = storage.all()["State" + '.' + state_id]
            if state.cities:
                for c in cities:
                    if c.state_id == state_id:
                        cities_list.append(c)
            return jsonify(cities_list.to_dict())
    abort(404)
