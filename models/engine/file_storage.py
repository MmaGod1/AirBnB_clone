#!/usr/bin/python3
"""Serializes instances to a JSON file and deserializes JSON to instances."""
import json
import os
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    """Serializing and deserializing objects to and from a JSON file."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary containing all stored objects."""
        return self.__objects

    def new(self, obj):
        """Adds a new object to the storage dictionary."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serializes the objects dictionary to a JSON file."""
        with open(self.__file_path, "w") as f:
            obj_items = self.__objects.items()
            obj_dict = {key: obj.to_dict() for key, obj in obj_items}
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file to the objects dictionary if it exists"""
        class_list = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Place": Place,
            "Amenity": Amenity,
            "Review": Review
        }
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, "r", encoding="UTF-8") as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    name = key.split('.')[0]
                    if name in class_list:
                        obj = class_list[name](**value)
                        self.__class__.__objects[key] = obj
