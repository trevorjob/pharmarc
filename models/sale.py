#!/usr/bin/python3
"""
Define the Sale class for the 'drugs' table in the database.
"""

import enum

from models import STORAGE
from models.base_model import BaseModel
from sqlalchemy import JSON, Enum
from sqlalchemy.ext.mutable import MutableList


class PaymentMethod(enum.Enum):
    CASH = "cash"
    CARD = "card"
    TRANSFER = "transfer"


class Sale(BaseModel, STORAGE.Model):
    """
    Table name in the database

    Attributes:
        __tablename__ (str): The name of the database table.
        total_price (float): The total_price of the sale. Required field.
        branch_id (str): The branch id of the sale. Required field.
        drug_ids (str): The drug_ids from the sale Required field.
        payment_method (str): the payment method to use for the sale. Required field.
        employee_id (str): The employee id of the sale. Required field.
        status (str): the status of the sale. Required field.
    """

    employee_id = STORAGE.Column(STORAGE.ForeignKey("employee.id"), nullable=False)

    branch_id = STORAGE.Column(STORAGE.ForeignKey("branch.id"), nullable=False)
    drug_ids = STORAGE.Column(MutableList.as_mutable(JSON))
    total_price = STORAGE.Column(STORAGE.Float, nullable=False)
    payment_method = STORAGE.Column(
        Enum(PaymentMethod),
        nullable=False,
        default=PaymentMethod(PaymentMethod.CASH.value),
    )
    status = STORAGE.Column(STORAGE.String(50), nullable=False, default="completed")

    def to_dict(self):
        """Convert Sale object to dictionary"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "branch_id": self.branch_id,
            "drug_ids": self.drug_ids,
            "total_price": self.total_price,
            "payment_method": self.payment_method.value,  # Convert enum to string
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
