#!/usr/bin/python3
"""
Define the Branch class for the 'Branches' table in the database.
"""

from models import STORAGE
from models.base_model import BaseModel


class Inventory(BaseModel, STORAGE.Model):
    """
    Model for the drugs in a certain branch

    Attributes:
        __tablename__ (str): The name of the database table.
        branch_id (str): The ID of the branch. Required field.
        drug_id (str): the drug ID. Required
        price (int): The price of the drug in the branch. Required field.
        quantity (int): The quantity of the drug. Required field.
        expiry_date (date): The date of the expiration. Required field."""

    branch_id = STORAGE.Column(
        STORAGE.String(128), STORAGE.ForeignKey("branch.id"), nullable=True
    )
    drug_id = STORAGE.Column(
        STORAGE.String(128), STORAGE.ForeignKey("drug.id"), nullable=True
    )
    quantity = STORAGE.Column(STORAGE.Integer, nullable=True)
    price = STORAGE.Column(STORAGE.Integer, nullable=True)
    expiry_date = STORAGE.Column(STORAGE.DateTime, nullable=True)

