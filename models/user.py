#!/usr/bin/python3
"""A class User that inherits from BaseModel"""
from model import BaseModel


class User(BaseModel):
    """Defines the first User class

    Attributes:
        email (str): The email of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    """
    def __init__(self):
        email = ""
        password = ""
        first_name = ""
        last_name = ""
