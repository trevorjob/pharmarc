#!/usr/bin/python3
"""all routes for the transfers"""
import json
from ast import literal_eval
from datetime import datetime
from uuid import uuid4

from api.views import app_views
from flask import abort, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from helpers.object import *
from models import STORAGE, check_branch_id, role_required
from models.branch import Branch
from models.inventory import Inventory
from models.transfer import Transfer, TransferDrug


@app_views.route("/transfers/general", methods=["GET"], strict_slashes=True)
@jwt_required()
@role_required()
def all_transfers():
    """get all transfers from transfer Table in the database"""
    transfers = STORAGE.all(Transfer)
    return jsonify({"data": [transfer.to_dict() for transfer in transfers]})


@app_views.route("/transfers/<id>", methods=["GET"], strict_slashes=True)
@jwt_required()
@role_required()
def get_transfer(id):
    """get transfer information for a given transfer id"""

    if not id:
        return abort(404, description="invalid transfer id")

    transfer = STORAGE.get(Transfer, id)
    if not transfer:
        return abort(404)
    return jsonify({"data": transfer.to_dict()})


@app_views.route("/transfers", methods=["GET"], strict_slashes=True)
@jwt_required()
@role_required()
def branch_transfers():
    """get all transfers from the branch"""
    branch_id = get_jwt_identity().get("branch_id")
    branch = STORAGE.get(Branch, branch_id)

    transfers = None
    search_date = request.args.get("search_date")
    if search_date:
        s = [
            br
            for br in branch.transfers_requested
            if datetime.strptime(str(br.created_at).split(" ")[0], "%Y-%m-%d").date()
            == datetime.strptime(search_date, "%Y-%m-%d").date()
        ]
        r = [
            br
            for br in branch.transfers_sent
            if datetime.strptime(str(br.created_at).split(" ")[0], "%Y-%m-%d").date()
            == datetime.strptime(search_date, "%Y-%m-%d").date()
        ]
        transfers = r + s

    else:
        transfers = branch.transfers_requested + branch.transfers_sent

    return jsonify([transfer.to_dict() for transfer in transfers])


@app_views.route("/transfers/request", methods=["POST"], strict_slashes=True)
@jwt_required()
@role_required()
def post_transfer():
    """add new transfer"""
    req = request.form.to_dict()  # req = request.get_json()
    branch_id = get_jwt_identity().get("branch_id")
    req = check_keys(
        req,
        [
            "transfer_requests",
            "sender_id",
        ],
    )
    validate_object(
        req,
        [
            "transfer_requests",
            "sender_id",
        ],
    )
    req["requester_id"] = branch_id
    req["employee_id"] = get_jwt_identity().get("id")
    transfer_requests = req.pop("transfer_requests")
    try:
        parsed_list = json.loads(transfer_requests)
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Failed to decode JSON: {e}"}), 400
    if not transfer_requests:
        return abort(404)

    t_r = literal_eval(transfer_requests)
    transfer = Transfer(**req)
    STORAGE.new(transfer)
    STORAGE.flush()
    for re in t_r:
        transfer_drug = TransferDrug(**re, transfer_id=transfer.id)
        transfer_drug.id = str(uuid4())
        STORAGE.new(transfer_drug)
        STORAGE.flush()

    STORAGE.save()
    t = STORAGE.get(Transfer, transfer.id)
    return (
        jsonify({"message": "successfully sent transfer request", "data": t.to_dict()}),
        201,
    )


@app_views.route("/transfers/<id>/approve", methods=["POST"], strict_slashes=True)
@jwt_required()
@role_required()
def eval_transfer_request(id):
    """approve a transfer request"""
    if not id:
        return abort(404, description="transfer id not found")

    transfer = STORAGE.get(Transfer, id)
    if not transfer:
        return abort(404, description="transfer request not found")

    transfer_items = transfer.items
    branch_id = get_jwt_identity().get("branch_id")
    if branch_id == transfer.requester_id:
        return abort(
            404, description="Request Denied. Approval must be from return branch"
        )
    for item in transfer_items:
        item_quantity = int(item.quantity)
        sender = branch_id
        requester = transfer.requester_id
        requester_drug = STORAGE.get_from_inventory(requester, item.drug_id)
        sender_drug = STORAGE.get_from_inventory(sender, item.drug_id)
        # print(sender_drug, requester_drug)
        if requester_drug is None:
            branch_drug = Inventory(
                branch_id=requester,
                drug_id=item.drug_id,
                quantity=item_quantity,
                price=sender_drug.price,
                expiry_date=sender_drug.expiry_date,
            )
            STORAGE.new(branch_drug)
            sender_drug.quantity -= item_quantity
            STORAGE.flush()

        else:
            sender_drug.quantity -= item_quantity
            requester_drug.quantity += item_quantity
            STORAGE.flush()

    transfer = STORAGE.get(Transfer, id)
    transfer.status = "approved"
    STORAGE.save()

    return jsonify({"message": "transfer successfully approved"})


@app_views.route("/transfers/<id>/reject", methods=["POST"], strict_slashes=True)
@jwt_required()
@role_required()
def reject_transfer_request(id):
    """reject a transfer request"""
    if not id:
        return abort(404, description="transfer id not found")

    transfer = STORAGE.get(Transfer, id)
    if not transfer:
        return abort(404, description="transfer request not found")
    branch_id = get_jwt_identity().get("branch_id")
    if branch_id == transfer.requester_id:
        return abort(
            404, description="Request Denied. Denial must be from return branch"
        )
    transfer.status = "rejected"
    STORAGE.save()
    return jsonify({"message": "transfer rejected successfully"})
