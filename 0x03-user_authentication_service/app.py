#!/usr/bin/env python3
"""app module
"""
from auth import Auth
from flask import Flask, jsonify, request

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
