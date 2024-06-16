#!/usr/bin/python3
"""Serializes instances to a JSON file and deserializes JSON to instances."""
import json
import os
from models.base_model import BaseModel

class FileStorage:
    """Serializing and deserializing objects to and from a JSON file."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary containing all stored objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Adds a new object to the storage dictionary."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes the objects dictionary to a JSON file."""
        obj_dict = {key: obj.to_dict() for key, obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file to the objects dictionary if it exists."""
        try:
            with open(FileStorage.__file_path, "r") as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    cls_name = value['__class__']
                    del value['__class__']
                    self.new(eval(cls_name)(**value))
        except FileNotFoundError:
            return
