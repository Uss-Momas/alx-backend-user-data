#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from os import getenv


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def login():
    """login route"""
    email = request.form.get("email", None)
    pwd = request.form.get("password", None)
    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if not pwd or len(pwd) == 0:
        return jsonify({"error": "password missing"}), 400
    from models.user import User
    users = User.search({"email": email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(pwd):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            resp.set_cookie(getenv('SESSION_NAME'), session_id)
            return resp
    return jsonify({"error": "wrong password"}), 401


@app_views.route("/auth_session/logout", methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """logout route"""
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({}), 200
