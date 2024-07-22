#!/usr/bin/python3
"""
Define the Transfer class for the 'Transfers' table in the database.
"""

from models import STORAGE
from models.base_model import BaseModel


class TransferDrug(BaseModel, STORAGE.Model):
    """
    Table name in the database

    Attributes:
        __tablename__ (str): The name of the database table.
        transfer_id (str): the transfer id for the transfer. Required field
        drug_id (str): the drug id. Required field
        quantity (int): the number of the drug to be transfered. Required field.
    """

    transfer_id = STORAGE.Column(STORAGE.ForeignKey("transfer.id"), nullable=True)
    drug_id = STORAGE.Column(STORAGE.ForeignKey("drug.id"), nullable=True)
    quantity = STORAGE.Column(STORAGE.Integer, nullable=True)


class Transfer(BaseModel, STORAGE.Model):
    """
    Table name in the database

    Attributes:
        __tablename__ (str): The name of the database table.
        employee_id (str): the employee that does the drug transfer. Required field
        from_branch_id (str): the branch the drug is transfered from. Required field
        to_branch_id (str): the branch the drug is transfered to. Required field
        status (str): the status of the transfer. Required field.
    """

    # __tablename__ = "transfer"
    employee_id = STORAGE.Column(STORAGE.ForeignKey("employee.id"), nullable=True)
    requester_id = STORAGE.Column(STORAGE.ForeignKey("branch.id"), nullable=True)
    sender_id = STORAGE.Column(STORAGE.ForeignKey("branch.id"), nullable=True)
    status = STORAGE.Column(STORAGE.String(128), nullable=True, default="pending")
    items = STORAGE.relationship("TransferDrug", backref="transfer")
