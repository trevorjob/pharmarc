#!/usr/bin/python3
"""all routes for the orders"""
import json

from api.views import app_views
from flask import abort, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from helpers.object import *
from models import STORAGE, check_branch_id, role_required
from models.order import Order, OrderStatus


@app_views.route("/orders", methods=["GET"], strict_slashes=True)
@jwt_required()
def all_orders():
    """get all orders from order Table in the database"""
    branch_id = get_jwt_identity().get('branch_id')
    orders = STORAGE.all_by_branch(Order, branch_id)

    return jsonify({"data": [order.to_dict() for order in orders]})


@app_views.route("/orders/<id>", methods=["GET"], strict_slashes=True)
@jwt_required()
def get_order(id):
    """get order information for a given order id"""

    if not id:
        return abort(400, description="invalid order id")

    order = STORAGE.get(Order, id)
    if not order:
        return abort(404, description="Order not found")

    return jsonify({"data": order.to_dict()})


@app_views.route("/suppliers/order", methods=["POST"], strict_slashes=True)
@jwt_required()
@role_required()
def post_order():
    """add new order"""
    # req = request.get_json()
    req = request.form.to_dict()
    branch_id = get_jwt_identity().get('branch_id')
    req = check_keys(
        req,
        [
            "products",
        ],
    )
    validate_object(
        req,
        [
            "products",
        ],
    )
    products = req.pop("products")
    dds = []
    try:
        parsed_list = json.loads(products)
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Failed to decode JSON: {e}"}), 400
    total_price = 0
    for drug_id in parsed_list:
        drug = STORAGE.get_from_inventory(branch_id, drug_id.get("id"))
        drug.quantity += int(drug_id.get("quantity"))
        price = int(drug.price) * int(drug_id.get("quantity"))
        total_price += price
        dds.append(drug.id)
        STORAGE.flush()

        order = Order(
            **req,
            branch_id=branch_id,
            total_cost=total_price,
            products=dds,
            status=OrderStatus("completed"),
        )

    STORAGE.new(order)
    STORAGE.save()
    ord = STORAGE.get(Order, order.id)

    return (
        jsonify({"message": "successfully created order", "data": ord.to_dict()}),
        201,
    )
