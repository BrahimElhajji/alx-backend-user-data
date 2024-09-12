#!/usr/bin/env python3
""" Flask app """

from flask import Flask, request, jsonify, abort, make_response
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index():
    """Basic route to return a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """Endpoint to register a new user."""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """Endpoint to log in a user and create a session."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Handles user logout by destroying the session."""
    email_ = request.form.get("email")
    try:
        reset = AUTH.get_reset_password_token(email_)
        return jsonify({"email": email_, "reset_token": reset}), 200
    except ValueError:
        abort(403) 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
