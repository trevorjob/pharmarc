from uuid import uuid4

from api.views import app_auth
from flask import abort, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from helpers.object import check_keys, validate_object
from models import STORAGE, blacklist
from models.branch import Branch
from models.employee import Employee
from werkzeug.security import check_password_hash, generate_password_hash


@app_auth.route("/register", methods=["POST"])
def signup_user():
    """create a new employee"""
    if not request.form.to_dict():
        abort(404, description="Not a valid json")

    req = request.form.to_dict()
    req = check_keys(
        req,
        [
            "email",
            "password",
            "firstName",
            "lastName",
            "is_admin",
            "branch_id",
            "phone_number",
        ],
    )
    validate_object(
        req,
        ["email", "password", "firstName", "lastName", "branch_id", "phone_number"],
    )

    employee = STORAGE.get_email(Employee, req["email"])
    if employee:
        return jsonify({"message": "this employee already exists"}), 400
    if "is_admin" in req:
        req["is_admin"] = bool(req["is_admin"])
    password = generate_password_hash(req["password"])
    req["password"] = password
    print(req)
    instance = Employee(**req)
    instance.id = str(uuid4())

    STORAGE.new(instance)
    STORAGE.save()
    uss = STORAGE.get(Employee, instance.id)

    accessToken = create_access_token(
        identity={"id": employee.id, "branch_id": employee.branch_id}
    )

    return (
        jsonify(
            {
                "message": "employee created successfully",
                "accessToken": accessToken,
                "data": uss.to_dict(),
            }
        ),
        201,
    )


@app_auth.route("/login", methods=["POST"])
def signin_user():
    """login a employee"""
    if not request.form.to_dict():
        abort(404, description="Not A Valid JSON")

    data = request.form.to_dict()
    req = check_keys(
        data,
        ["email", "password"],
    )
    validate_object(
        req,
        ["email", "password"],
    )
    employee = STORAGE.get_email(Employee, req["email"])
    if not employee:
        abort(404, "invalid email address")
    if check_password_hash(employee.password, req["password"]):
        accessToken = create_access_token(
            identity={"id": employee.id, "branch_id": employee.branch_id}
        )
        return (
            jsonify({"message": "log in successfull", "access_token": accessToken}),
            200,
        )
    else:
        return jsonify({"message": "password is incorrect"}), 404


@app_auth.route("/logout", methods=["POST"])
@jwt_required()
def signout_user():
    """logout a employee"""
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({"message": "logged out successfully"})


@app_auth.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """get current loggout in employee"""
    curr = get_jwt_identity().get("id")
    employee = STORAGE.get(Employee, curr)
    branch = employee.branch
    emp = employee.to_dict()
    emp["branch"] = branch.to_dict()
    emp.pop("branch_id")
    return jsonify({"data": emp}), 200


@app_auth.route("/me", methods=["PUT"], strict_slashes=True)
@jwt_required()
def update_employee():
    """Update an employee's information"""
    curr = get_jwt_identity().get("id")
    employee = STORAGE.get(Employee, curr)
    if employee is None:
        return abort(404)

    data = request.form.to_dict()
    if not data:
        return abort(400, description="Not a JSON")

    # Update allowed fields
    data = check_keys(data, ["firstName", "lastName", "phone_number"])
    for key, value in data.items():
        setattr(employee, key, value)

    STORAGE.save()
    em = STORAGE.get(Employee, curr)
    return jsonify({"data": em.to_dict()}), 200


@app_auth.route("/me", methods=["DELETE"], strict_slashes=True)
@jwt_required()
def delete_employee():
    """Delete an employee"""
    curr = get_jwt_identity().get("id")
    employee = STORAGE.get(Employee, curr)
    if employee is None:
        return abort(404)

    STORAGE.delete(employee)
    STORAGE.save()
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({"message": "employee deleted successfully"}), 200
