#!/usr/bin/python3
"""Defines the BaseModel class."""
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents the parent model for all other model for this project."""
    def __init__(self, *args, **kwargs):
        """Initialize instances of BaseModel."""
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.fromisoformat(value)
        if key != '__class__':
            setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def save(self):
        """updates the updated_at attribute with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary of the BaseModel

        the dictionary includes the key-value pair, and
        a __class__ key indicating the class name.
        """
        micro = 'microseconds'
        inst_dict = self.__dict__.copy()
        inst_dict['__class__'] = self.__class__.__name__
        inst_dict['created_at'] = self.created_at.isoformat(timespec=micro)
        inst_dict['updated_at'] = self.updated_at.isofor(timespec=micro)
        return inst_dict

    def __str__(self):
        """Return the str representation of the BaseModel instance."""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
