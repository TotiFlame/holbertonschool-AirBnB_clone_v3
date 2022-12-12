#!/usr/bin/python3
"""
Create a new view for State objects
"""


from flask import Flask, jsonify, abort, request
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


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
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


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_st():
    """
    - Creates a State
    - If the HTTP body request is not valid JSON,
    raise a 400 error with the message Not a JSON
    - If the dictionary doesn’t contain the key name,
    raise a 400 error with the message Missing name
    """
    state = request.get_json(silent=True)
    if state is None:
        abort(400, 'Not a JSON')
    if "name" not in state:
        abort(400, 'Missing name')
    new_st = State(**state)
    new_st.save()
    return jsonify(new_st.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_st(state_id):
    """
    - Updates a State
    - If the state_id is not linked to any State object, raise a 404 error
    - If not vlid json, raise a 400 error with the message Not a JSON
    - Update the State object with all key-value pairs of the dictionary.
    - Returns the State object with the status code 200
    """
    state_and_id = storage.get(State, state_id)
    state = request.get_json(silent=True)

    if state_and_id is None:
        abort(404)
    if state is None:
        abort(400, 'Not a JSON')

    for key, value in state.items():
        if key in ['id', 'created_at', 'updated_at']:
            pass
        setattr(state_and_id, key, value)
    state_and_id.save()
    return jsonify(state_and_id.to_dict()), 200
