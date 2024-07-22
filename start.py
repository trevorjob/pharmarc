#!/usr/bin/python3
""" Flask Application """

from api.views import app_views, app_auth
from flask import jsonify
from models import STORAGE, app

app.register_blueprint(app_views)
app.register_blueprint(app_auth)
with app.app_context():
    STORAGE.create_all()


def errFormat(err):
    er = str(err)
    return er.split(": ")[1]


@app.errorhandler(404)
def not_found(error):
    """404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return jsonify({"error": errFormat(error)}), 404


@app.errorhandler(401)
def not_found(error):
    """404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return jsonify({"error": errFormat(error)}), 401


@app.errorhandler(400)
def bad_req(error):
    """400 Error
    ---
    responses:
      404:
        description: string
    """
    return jsonify({"error": errFormat(error)}), 400


@app.errorhandler(403)
def bad_req(error):
    """400 Error
    ---
    responses:
      404:
        description: string
    """
    return jsonify({"error": errFormat(error)}), 403


if __name__ == "__main__":
    """Main Function"""
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)
