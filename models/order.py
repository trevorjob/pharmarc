import enum
from datetime import datetime

from models import STORAGE
from models.base_model import BaseModel
from sqlalchemy import JSON, DateTime, Enum, Float
from sqlalchemy.ext.mutable import MutableList


class OrderStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"


class Order(BaseModel, STORAGE.Model):
    """
    Table name in the database

    Attributes:
        __tablename__ (str): The name of the database table.
        supplier_id (str): The supplier id for the order. Required field.
        products (list): The list of products in the order. Required field.
        total_cost (float): The total cost of the order. Required field.
        status (str): The status of the order. Required field.
    """

    # __tablename__ = "orders"

    supplier = STORAGE.Column(
        STORAGE.String(128), nullable=False, default="Maxwells limited"
    )
    products = STORAGE.Column(MutableList.as_mutable(JSON), nullable=False)
    total_cost = STORAGE.Column(STORAGE.Float, nullable=False)
    status = STORAGE.Column(
        Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False
    )
    branch_id = STORAGE.Column(
        STORAGE.String(128), STORAGE.ForeignKey("branch.id"), nullable=True
    )
    

    def to_dict(self):
        """Convert Sale object to dictionary"""
        return {
            "id": self.id,
            "supplier": self.supplier,
            "branch_id": self.branch_id,
            "products": self.products,
            "total_cost": self.total_cost,
            "status": self.status.value,  # Convert enum to string
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
