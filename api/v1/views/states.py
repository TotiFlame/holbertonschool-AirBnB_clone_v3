#!/usr/bin/python3
"""
Create a new view for State objects
"""


from flask import Flask, jsonify, abort
from models import state, storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_list():
    """
    - Retrieves the list of all State objects and to json
    """
    n_dict = []
    _list = storage.all("State").values()
    for state in _list:
        n_dict.append(state.to_dict())
    return jsonify(n_dict)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def show_one_state(state_id):
    """
    - Retrieves a State object
    - if the state id isnt linked to any state object, raise a 404 error
    """
    state = storage.get(State, state_id)
    if state is not None:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """
    - Deletes a State object
    - if the state id isnt linked to any state object, raise a 404 error
    - Returns an empty dictionary with the status code 200
    """
    states = storage.all("State").values()
    for state in states:
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
    abort(404)

# @app_views.route('/states', methods=['POST'], strict_slashes=False)


# @app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)