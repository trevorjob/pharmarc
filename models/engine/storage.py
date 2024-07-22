#!/usr/bin/python3

"""storage class"""

from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Storage(SQLAlchemy):
    """Storage  implementation for database"""

    def __init__(
        self,
        app: Flask | None = None,
    ):
        """intialize database"""
        super().__init__(
            app,
        )

    def save(self):
        """commit all changes of the current database session"""

        self.session.commit()

    def flush(self):
        """flush all changes of the current database session"""
        self.session.flush()

    def remove(self):
        """remove all changes of the current database session"""
        self.session.remove()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.session.delete(obj)

    def all(self, cls=None, id=None):
        """get all models from the database"""
        if cls is not None:
            if id is not None:
                return (
                    self.session.execute(self.select(cls).where(cls.id == id))
                    .scalars()
                    .all()
                )
        return [val for val in self.session.execute(self.select(cls)).scalars().all()]

    def all_by_branch(self, cls, branch_id):
        """get all models from the database"""
        if cls is not None:
            if id is not None:
                return (
                    self.session.execute(
                        self.select(cls).where(cls.branch_id == branch_id)
                    )
                    .scalars()
                    .all()
                )
        return [val for val in self.session.execute(self.select(cls)).scalars().all()]

    def all_by_send(self, cls, branch_id):
        """get all models from the database"""
        if cls is not None:
            if id is not None:
                return (
                    self.session.execute(
                        self.select(cls).where(cls.branch_id == branch_id)
                    )
                    .scalars()
                    .all()
                )
        return [val for val in self.session.execute(self.select(cls)).scalars().all()]

    def all_by_transfer(self, cls, transfer_id):
        """get all models from the database"""
        if cls is not None:
            if id is not None:
                return (
                    self.session.execute(
                        self.select(cls).where(cls.transfer_id == transfer_id)
                    )
                    .scalars()
                    .all()
                )
        return [val for val in self.session.execute(self.select(cls)).scalars().all()]

    def new(self, *obj):
        """add the object to the current database session"""
        return [self.session.add(ob) for ob in obj]

        # self.session.add(obj)

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """

        val = self.session.execute(self.select(cls).where(cls.id == id)).scalar()
        if val:
            return val
        else:
            return None

    def get_from_inventory(self, branch_id, drug_id):
        """Returns the quantity of the drug"""
        # self.remove()
        from models.inventory import Inventory

        branch_drug_entry = self.session.execute(
            self.select(Inventory).where(Inventory.drug_id == drug_id)
        ).scalars()
        b = ""
        for branch in branch_drug_entry:
            if branch.branch_id == branch_id:
                b = branch

        if b:
            return b
        else:
            return None

    def get_by_date(self, cls, branch_id, search_date):
        """Returns a list of objects that match that date"""
        formatted_date = datetime.strptime(search_date, "%m-%d-%Y").date()
        transfers = (
            self.session.execute(
                self.select(cls).where(
                    cls.created_at == formatted_date and cls.branch_id == branch_id
                )
            )
            .scalars()
            .all()
        )

        return transfers

    def get_email(self, cls, email):
        """
        Returns the object based on the class name and its email, or
        None if not found
        """

        val = self.session.execute(self.select(cls).where(cls.email == email)).scalar()
        if val:
            return val
        else:
            return None

    def update_quantity(self, branch_id, drug_id, new_quantity):
        from models.branch import Inventory

        branch_drug_entry = (
            self.session.query(Inventory)
            .filter_by(branch_id=branch_id, drug_id=drug_id)
            .first()
        )
        if branch_drug_entry:
            branch_drug_entry.quantity = new_quantity
            self.save()
            return True
        else:
            return False

    # def get_druginv(self, branch_id, drug_id, new_quantity):
    #     from models.branch import Inventory

    #     branch_drug_entry = (
    #         self.session.query(Inventory)
    #         .filter_by(branch_id=branch_id, drug_id=drug_id)
    #         .first()
    #     )
    #     if branch_drug_entry:
    #         branch_drug_entry.quantity = new_quantity
    #         self.save()
    #         return True
    #     else:
    #         return False
