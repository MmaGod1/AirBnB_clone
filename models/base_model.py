#!/usr/bin/python3
"""Defines the BaseModel class."""
import models
from uuid import uuid4


class BaseModel:
  """Represents the parent class gor all other classes for the AirBnB console project."""
  
  def __init__(self):
    """Initialize instances of BaseModel."""
    self.id = str(uuid4())
    
