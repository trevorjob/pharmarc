#!/usr/bin/python3

"""Base class"""
from uuid import uuid4

from models import STORAGE
from datetime import datetime

time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """Base class from which future classes will be derived"""

    __abstract__ = True
    id = STORAGE.Column(
        STORAGE.String(60),
        primary_key=True,
        default=lambda: str(uuid4()),
        nullable=False,
    )
    created_at = STORAGE.Column(
        STORAGE.DateTime, default=datetime.utcnow(), nullable=False
    )

    updated_at = STORAGE.Column(STORAGE.DateTime, default=datetime.utcnow())

    def __repr__(self):
        """Representation of the Base object."""
        return f"{self.__class__.__name__}->{self.to_dict()}"

    def to_dict(self, save_fs=None):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if save_fs is None:
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict
