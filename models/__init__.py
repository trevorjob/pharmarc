#!/usr/bin/python3
"""handle database models connection"""

import os
from functools import wraps

from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from models.engine.storage import Storage
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from datetime import timedelta

# from models.engine.storage import Storage


app = Flask(__name__)
# CORS(
#     app,
#     resources={
#         r"/api/*": {"origins": "*"},
#         r"/auth/*": {"origins": "*"},
#     },
#     supports_credentials=True,
# )

# Database Configuration
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True  # Use this if serving over HTTPS

# Secret Key
app.config["SECRET_KEY"] = os.environ.get("DB_SECRET_KEY", "sqlite:///site.db")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI", "sqlite:///site.db")
app.config["SESSION_PROTECTION"] = "strong"
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_TOKEN", "your_jwt_secret_key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
STORAGE = Storage(app)
jwt = JWTManager(app)
blacklist = set()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blacklist


def check_branch_id(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from models.branch import Branch

        branch_id = request.headers.get("branch-id")
        if not branch_id:
            return jsonify({"error": "branch-id header is missing"}), 400

        branch = STORAGE.get(Branch, branch_id)
        if branch is None:
            return abort(404, description="Invalid branch-id")

        return f(*args, **kwargs)

    return decorated_function


# Decorator to check if the current employee has the required role
def role_required():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            from models.employee import Employee

            current_employee = get_jwt_identity().get("id")
            employee = STORAGE.get(Employee, current_employee)
            if not employee or not bool(employee.is_admin):
                return (
                    jsonify({"error": "Access forbidden: Insufficient permissions"}),
                    403,
                )
            return f(*args, **kwargs)

        return wrapper

    return decorator
