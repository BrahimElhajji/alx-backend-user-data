#!/usr/bin/env python3
""" Module of the API """
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth


app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)

# Initialize auth based on AUTH_TYPE environment variable
auth = None
auth_type = getenv('AUTH_TYPE')

if auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == "session_auth":
    auth = SessionAuth()


@app.before_request
def require_auth():
    """
    Method to enforce authentication.
    """
    excluded_paths = ['/api/v1/status', '/api/v1/auth_session/login/']

    if request.path not in excluded_paths:
        if not (auth.authorization_header(request)
                or auth.session_cookie(request)):
            abort(401)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    app.run(host=getenv('API_HOST', '0.0.0.0'),
            port=int(getenv('API_PORT', 5000)))
