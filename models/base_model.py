#!/usr/bin/python3
"""Defines the BaseModel class."""
from uuid import uuid4
from datetime import datetime

class BaseModel:
  """Represents the parent class for all other classes for the AirBnB console project."""
  
  def __init__(self):
    """Initialize instances of BaseModel."""
    self.id = str(uuid4())
    self.created_at = datetime.now()
    self.updated_at = datetime.now()
  def save(self):
    """updates the updated_at attribute with the current datetime"""
    self.updated_at = datetime.now()

mytest = BaseModel()
print(mytest.id)
print(mytest.created_at)
