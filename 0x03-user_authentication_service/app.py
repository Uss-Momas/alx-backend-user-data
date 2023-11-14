#!/usr/bin/env python3
"""app module
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

AUTH = Auth()

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def main():
    """main route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", strict_slashes=False, methods=["POST"])
def post_user():
    """creates a new user route"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": user.email, "message": "user created"})


@app.route("/sessions", strict_slashes=False, methods=['POST'])
def login():
    """login route
    """
    email = request.form.get("email")
    pwd = request.form.get("password")
    if not email or not pwd:
        abort(401)
    if AUTH.valid_login(email, pwd):
        session_id = AUTH.create_session(email)
        if session_id:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie('session_id', session_id)
            return response
        abort(401)
    abort(401)


@app.route("/sessions", strict_slashes=False, methods=["DELETE"])
def logout():
    """logout route
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", strict_slashes=False)
def profile():
    """profile route"""
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email})


@app.route("/reset_password", strict_slashes=False, methods=["POST"])
def get_reset_password_token():
    """get_reset_password_token route"""
    email = request.form.get("email")
    if email is None:
        abort(403)
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": token})


@app.route("/reset_password", strict_slashes=False, methods=['PUT'])
def update_password():
    """update_password route"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_pwd = request.form.get("new_password")

    if not email or not reset_token or not new_pwd:
        abort(403)
        try:
            AUTH.update_password(reset_token, new_pwd)
        except ValueError:
            abort(403)
        return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
