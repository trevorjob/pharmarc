#!/usr/bin/python3
"""all routes for the drugs"""
from datetime import datetime

from api.views import app_views
from flask import abort, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from helpers.object import *
from models import STORAGE, check_branch_id
from models.branch import Branch
from models.drug import Drug
from models.inventory import Inventory


@app_views.route("/drugs/general", methods=["GET"], strict_slashes=True)
@jwt_required()
def all_drugs():
    """get all drugs from drug Table in the database"""
    drugs = STORAGE.all(Drug)
    return jsonify({'data': [drug.to_dict() for drug in drugs]})


@app_views.route("/drugs", methods=["GET"], strict_slashes=True)
@jwt_required()
def branch_drugs():
    """get all drugs from the branch"""
    # params
    branch_id = get_jwt_identity().get('branch_id')
    branch = STORAGE.get(Branch, branch_id)

    if branch is None:
        return abort(404, description="invalid branch id")
    # Get query parameters
    search_query = request.args.get("q")
    expiry_date_from = request.args.get("expiry_date_from")
    expiry_date_to = request.args.get("expiry_date_to")

    # Convert date strings to datetime objects
    if expiry_date_from:
        expiry_date_from = datetime.strptime(expiry_date_from, "%Y-%m-%d")
    if expiry_date_to:
        expiry_date_to = datetime.strptime(expiry_date_to, "%Y-%m-%d")
    drugs = branch.drugs
    fullDrugs = []
    # Filter drugs based on query parameters
    if search_query or expiry_date_from or expiry_date_to:
        filtered_drugs = []
        for drug in drugs:
            q = STORAGE.get_from_inventory(branch.id, drug.drug_id)
            dru = STORAGE.get(Drug, drug.drug_id)
            if dru is None:
                return abort(404)

            # Apply search and filter conditions
            matches_search = (
                not search_query or search_query.lower() in dru.name.lower()
            )
            matches_expiry_from = (
                not expiry_date_from or q.expiry_date >= expiry_date_from
            )
            matches_expiry_to = not expiry_date_to or q.expiry_date <= expiry_date_to

            if matches_search and matches_expiry_from and matches_expiry_to:
                dictDrug = dru.to_dict()
                dictDrug["quantity"] = q.quantity
                dictDrug["price"] = q.price
                dictDrug["expiry_date"] = q.expiry_date
                filtered_drugs.append(dictDrug)

        fullDrugs = filtered_drugs
    else:
        fullDrugs = []
        for drug in drugs:
            q = STORAGE.get_from_inventory(branch.id, drug.drug_id)
            dru = STORAGE.get(Drug, drug.drug_id)
            if dru is None:
                return abort(404)
            dictDrug = dru.to_dict()
            dictDrug["quantity"] = q.quantity
            dictDrug["price"] = q.price
            dictDrug["expiry_date"] = q.expiry_date
            fullDrugs.append(dictDrug)

    return jsonify({"data": fullDrugs})


@app_views.route("/drugs/<id>", methods=["GET"], strict_slashes=True)
@jwt_required()
def get_drug(id):
    """get drug information for a given drug id"""
    branch_id = get_jwt_identity().get('branch_id')
    dru = STORAGE.get(Drug, id)
    if not dru:
        return abort(404, description="drug not found")
    drug = dru.to_dict()
    q = STORAGE.get_from_inventory(branch_id, dru.id)
    drug["quantity"] = q.quantity
    drug["price"] = q.price
    drug["expiry_date"] = q.expiry_date

    return jsonify({"data": drug})


@app_views.route("/drugs", methods=["POST"], strict_slashes=True)
@jwt_required()
def post_drug():
    """add new drug"""

    # req = request.get_json()
    req = request.form.to_dict()
    branch_id = get_jwt_identity().get('branch_id')

    req = check_keys(
        req,
        [
            "name",
            "quantity",
            "price",
            "expiry_date",
        ],
    )
    validate_object(
        req,
        [
            "name",
            "quantity",
            "price",
            "expiry_date",
        ],
    )
    quantity = req.pop("quantity")
    price = req.pop("price")
    expiry_date = req.pop("expiry_date")
    expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")

    drug = Drug(**req)
    STORAGE.new(drug)
    STORAGE.flush()
    # branches = STORAGE.all(Branch)
    branch_drug = Inventory(
        branch_id=branch_id,
        drug_id=drug.id,
        quantity=quantity,
        price=price,
        expiry_date=expiry_date.date(),
    )
    STORAGE.new(branch_drug)
    STORAGE.save()
    # STORAGE.update_quantity(branch.id, drug.id, quantity)
    d = STORAGE.get(Drug, drug.id)
    d = d.to_dict()
    d["quantity"] = quantity
    d["price"] = price
    d["expiry_date"] = expiry_date.date()

    return jsonify({"message": "successfully created drug", "data": d}), 201
