#!/usr/bin/python3
"""all routes for the sales"""
from api.views import app_views
from flask import abort, jsonify, request
from models import STORAGE, check_branch_id
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.sale import Sale, PaymentMethod
from models.drug import Drug
from helpers.object import *
import json


@app_views.route("/sales", methods=["GET"], strict_slashes=True)
@jwt_required()
def all_sales():
    """get all sales from sale Table in the database"""
    branch_id = get_jwt_identity().get("branch_id")
    sales = STORAGE.all_by_branch(Sale, branch_id)

    return jsonify({"data": [sale.to_dict() for sale in sales]})


@app_views.route("/sales/<id>", methods=["GET"], strict_slashes=True)
@jwt_required()
def get_sale(id):
    """get sale information for a given sale id"""

    if not id:
        return abort(404)

    sale = STORAGE.get(Sale, id)
    if not sale:
        return abort(404)

    return jsonify({"data": sale.to_dict()})


@app_views.route("/sales", methods=["POST"], strict_slashes=True)
@jwt_required()
def post_sale():
    """add new sale"""

    # req = request.get_json()
    req = request.form.to_dict()
    branch_id = get_jwt_identity().get("branch_id")
    req = check_keys(
        req,
        [
            "drug_ids",
            "payment_method",
        ],
    )
    validate_object(
        req,
        [
            "drug_ids",
        ],
    )
    req["employee_id"] = get_jwt_identity().get("id")
    drug_ids = req.pop("drug_ids")
    payment = None
    if req.get("payment_method"):
        payment = req.pop("payment_method")
    dds = []
    try:
        parsed_list = json.loads(drug_ids)
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Failed to decode JSON: {e}"}), 400
    total_price = 0
    for drug_id in parsed_list:
        drug = STORAGE.get_from_inventory(branch_id, drug_id.get("id"))
        if drug is None:
            return abort(404, description=f"could not find drug with id: {drug_id}")
        drug.quantity -= int(drug_id.get("quantity"))
        price = int(drug.price) * int(drug_id.get("quantity"))
        total_price += price
        dds.append(drug.id)
        STORAGE.flush()

    if payment is None:
        sale = Sale(**req, branch_id=branch_id, total_price=total_price, drug_ids=dds)
    else:
        sale = Sale(
            **req,
            branch_id=branch_id,
            total_price=total_price,
            drug_ids=dds,
            payment_method=PaymentMethod(payment),
        )

    STORAGE.new(sale)
    STORAGE.save()
    sl = STORAGE.get(Sale, sale.id)

    return jsonify({"message": "successfully created sale", "data": sl.to_dict()}), 201
