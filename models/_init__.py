#!/usr/bin/python3
"""Create a unique FileStorage instance for your application"""
from models.engine import file_storage

# Create a unique FileStorage instance
storage = file_storage.FileStorage()

# Call reload() method on the storage variable
storage.reload()

