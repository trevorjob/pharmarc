#!/usr/bin/python3
"""
Define the Branch class for the 'Branches' table in the database.
"""

from models import STORAGE
from models.base_model import BaseModel


class Branch(BaseModel, STORAGE.Model):
    """
    Table name in the database

    Attributes:
        __tablename__ (str): The name of the database table.
        location (str): The location of the branch. Required field.
        name (str): The name of the branch. Required
        phone (str): The phone number to the branch. Required field.
    """

    __tablename__ = "branch"
    location = STORAGE.Column(STORAGE.String(128), nullable=True)
    name = STORAGE.Column(STORAGE.String(128), nullable=True)
    drugs = STORAGE.relationship("Inventory", backref="branches")
    orders = STORAGE.relationship("Order", backref="branch")
    sales = STORAGE.relationship("Sale", backref="branch")
    employees = STORAGE.relationship("Employee", backref="branch")
    phone = STORAGE.Column(STORAGE.String(128), nullable=True)
    transfers_requested = STORAGE.relationship(
        "Transfer", foreign_keys="[Transfer.requester_id]", backref="requester_branch"
    )
    transfers_sent = STORAGE.relationship(
        "Transfer", foreign_keys="[Transfer.sender_id]", backref="sender_branch"
    )
