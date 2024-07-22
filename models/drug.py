#!/usr/bin/python3
"""
Define the Drug class for the 'drugs' table in the database.
"""

from models import STORAGE
from models.base_model import BaseModel



class Drug(BaseModel, STORAGE.Model):
    """
    Table name in the database

    Attributes:
        __tablename__ (str): The name of the database table.
        price (int): The price of the drug. Required field.
        name (str): The name of the Drug. Required
        expireyDate (date): The expireyDate date to the drug. Required field.
    """

    __tablename__ = "drug"
    name = STORAGE.Column(STORAGE.String(128), nullable=True)
    branches = STORAGE.relationship("Inventory", backref="drugs")
