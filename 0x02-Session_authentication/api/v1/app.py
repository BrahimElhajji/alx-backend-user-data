#!/usr/bin/env python3
""" Module of the API """
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS, cross_origin
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from models import storage


app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)

auth = None
auth_type = getenv('AUTH_TYPE')

if auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.before_request
def before_request():
    """Before each request handler"""
    if auth is None:
        return
    request.current_user = auth.current_user(request)
    if not auth.require_auth(request.path, ['/api/v1/status/',
                                            '/api/v1/unauthorized/',
                                            '/api/v1/forbidden/']):
        return
    if auth.authorization_header(request) is None:
        return jsonify({"error": "Unauthorized"}), 401
    if request.current_user is None:
        return jsonify({"error": "Forbidden"}), 403


@app.teardown_appcontext
def teardown_db(exception):
    """Close storage on app context teardown"""
    storage.close()


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=int(port))
