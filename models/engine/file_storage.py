#!/usr/bin/python3
"""Serializes instances to a JSON file and deserializes JSON to instances"""
import json


class FileStorage:
    """Serializing and deserialing objects to and from a JSON file."""

    __file_path: str = "file.json"
    __objects: dict = {}

    def all(self):
        """Returns the dictionary containing all stored objects."""
        return self.__objects

    def new(self, obj):
        """Adds a new object to the storage dictionary."""
        cls_name = obj.__class__.__name__
        obj_id = obj.id
        key = f"{cls_name}.{obj_id}"
        self.__objects[key] = obj

    def save(self):
        """Serializes the objects dictionary to a JSON file."""
        with open(self.__file_path, "w") as f:
            json.dump(self.__objects, f, indent=4)

    def reload(self):
        """Deserializes the JSON file to the objects dict if it exists."""
        try:
            with open(self.__file_path, "r") as f:
                self.__objects = json.load(f)
        except FileNotFoundError:
            pass
