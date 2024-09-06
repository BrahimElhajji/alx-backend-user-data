#!/usr/bin/env python3
"""
view to handle all routes for the Session authentication
"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import getenv
from api.v1.app import auth


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def sesh_login():
    """
    Handle user login with session authentication.
    """
    usr_email = request.form.get("email")
    usr_pass = request.form.get("password")

    if not usr_email:
        return jsonify({"error": "email missing"}), 400

    if not usr_pass:
        return jsonify({"error": "password missing"}), 400

    search_res = User.search({"email": usr_email})
    if not search_res:
        return jsonify({"error": "no user found for this email"}), 404

    my_usr = search_res[0]

    if not my_usr.is_valid_password(usr_pass):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(my_usr.id)
    response = jsonify(my_usr.to_json())

    session_name = getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response


@app_views.route("/auth_session/logout",
                 methods=['DELETE'], strict_slashes=False)
def sesh_logout():
    """
    Handle user logout by destroying the session.
    """
    if not auth.destroy_session(request):
        abort(404)
    else:
        return jsonify({}), 200
