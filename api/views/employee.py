#!/usr/bin/python3
"""all routes for the employees"""
from api.views import app_views
from flask import abort, jsonify, request
from helpers.object import *
from models import STORAGE, check_branch_id, role_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.branch import Branch
from models.employee import Employee


@app_views.route("/employees/general", methods=["GET"], strict_slashes=True)
@jwt_required()
@role_required()
def all_employees():
    """get all employees from employee Table in the database"""
    employees = STORAGE.all(Employee)
    return jsonify({"data": [employee.to_dict() for employee in employees]})


@app_views.route("/employees/<id>", methods=["GET"], strict_slashes=True)
@jwt_required()
@role_required()
def get_employee(id):
    """get employee information for a given employee id"""

    if not id:
        return abort(404)

    employee = STORAGE.get(Employee, id)
    if not employee:
        return abort(404, description="Employee not found")
    branch = employee.branch
    emp = employee.to_dict()
    emp["branch"] = branch.to_dict()
    return jsonify({"data": emp})


@app_views.route("/employees", methods=["GET"], strict_slashes=True)
@jwt_required()
@role_required()
def branch_employees():
    """get all employees from the branch"""
    branch_id = get_jwt_identity().get('branch_id')
    branch = STORAGE.get(Branch, branch_id)
    if branch is None:
        return abort(404)

    employees = branch.employees

    return jsonify({"data": [employee.to_dict() for employee in employees]})
