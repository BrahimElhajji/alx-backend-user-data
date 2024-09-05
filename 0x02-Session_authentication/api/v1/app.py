#!/usr/bin/env python3
""" Module of the API """
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS, cross_origin
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth


app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)

auth = None
auth_type = getenv('AUTH_TYPE')

if auth_type == "basic_auth":
    auth = BasicAuth()


@app.before_request
def before_request():
    """ Before request handler to run before each request """
    if auth is None:
        return
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_paths):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)


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
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
