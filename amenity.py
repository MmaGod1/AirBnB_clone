#!/usr/bin/python3
"""Definesthe Amenity class"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represents the amenities

    Attributes:
    name (str): The name of the Amenity. 
    """
    name = ""
