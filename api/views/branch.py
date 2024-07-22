#!/usr/bin/python3
"""all routes for the branches"""
from flask import abort, jsonify, request
from flask_jwt_extended import jwt_required

from api.views import app_views
from helpers.object import *
from models import STORAGE, role_required
from models.branch import Branch
from models.employee import Employee


@app_views.route("/branches", methods=["GET"], strict_slashes=True)
def all_branches():
    """get all branches from branch Table in the database"""
    branches = STORAGE.all(Branch)

    return jsonify({"data": [branch.to_dict() for branch in branches]})


@app_views.route("/branches/<id>", methods=["GET"], strict_slashes=True)
@jwt_required()
@role_required()
def get_branch(id):
    """get branch information for a given branch id"""

    branch = STORAGE.get(Branch, id)
    if not branch:
        return abort(404, description="Branch not found")

    # employees = STORAGE.all_by_branch(Employee, branch.id)
    employees = branch.employees
    ee = [employee.to_dict() for employee in employees]
    branchFull = branch.to_dict()
    branchFull["employees"] = ee
    return jsonify({"data": branchFull})


# @jwt_required()
# @role_required()
@app_views.route("/branches", methods=["POST"], strict_slashes=True)
def post_branch():
    """add new branch"""

    # req = request.get_json()
    req = request.form.to_dict()
    req = check_keys(
        req,
        [
            "name",
            "phone",
            "location",
        ],
    )
    validate_object(
        req,
        [
            "name",
            "phone",
            "location",
        ],
    )
    branch = Branch(**req)

    STORAGE.new(branch)
    STORAGE.save()
    val = STORAGE.get(Branch, branch.id)

    return (
        jsonify({"message": "successfully created branch", "data": val.to_dict()}),
        201,
    )
