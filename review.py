#!/usr/bin/python3
"""Defines a Review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represents the users review
    
    Attributes:
        place_id (str): for the place id.
        user_id (str): yhe iser id.
        text (str): the user Review
   """
   place_id = ""
   user_id = ""
   text = ""
