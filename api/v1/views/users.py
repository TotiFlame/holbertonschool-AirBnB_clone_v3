#!/usr/bin/python3
"""
Create a new view for User objects
"""


from flask import Flask, jsonify, abort, request
from models import user, storage
from models.user import User
from api.v1.views import app_views


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def show_all():
    user_list = []
    use = storage.all("User").values()
    if use is None:
        abort(404)
    for users in use:
        user_list.append(users.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def show_one_us(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_one(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    user = request.get_json(silent=True)
    if user is None:
        abort(400, 'Not a JSON')
    if "email" not in user:
        abort(400, 'Missing email')
    if "password" not in user:
        abort(400, 'Missing password')
    new_user = User(**user)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_us(user_id):
    user_and_id = storage.get(User, user_id)
    use = request.get_json(silent=True)

    if user_and_id is None:
        abort(404)
    if use is None:
        abort(400, 'Not a JSON')

    for key, value in use.items():
        if key in ['id','email', 'created_at', 'updated_at']:
            pass
        setattr(user_and_id, key, value)
    user_and_id.save()
    return jsonify(user_and_id.to_dict()), 200