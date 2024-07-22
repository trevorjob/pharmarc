#!/usr/bin/python3
"""
Define the Employee class for the 'employee' table in the database.
"""

from models import STORAGE
from models.base_model import BaseModel

# from flask import fore


class Employee(BaseModel, STORAGE.Model):
    """
    Table name in the database

    Attributes:
        __tablename__ (str): The name of the database table.
        email (str): The email address of the employee. Required field.
        firstName (str): The first name of the employee. Required field.
        lastName (str): The last name of the employee. Required field.
        password (str): The hashed password of the employee. Required field.
        isAdmin (bool): Whether the employee is an administrator
    """

    __tablename__ = "employee"
    firstName = STORAGE.Column(STORAGE.String(128), nullable=True)
    lastName = STORAGE.Column(STORAGE.String(128), nullable=True)
    email = STORAGE.Column(STORAGE.String(128), nullable=True, unique=True)
    phone_number = STORAGE.Column(STORAGE.String(128), nullable=True)
    password = STORAGE.Column(STORAGE.String(128), nullable=True)
    is_admin = STORAGE.Column(STORAGE.Boolean, nullable=True, default=False)
    branch_id = STORAGE.Column(STORAGE.ForeignKey("branch.id"), nullable=True)

    def is_active(self):
        # Define your own logic for determining if the employee is active or not
        return True

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

    def is_anonymous(self):
        return False
