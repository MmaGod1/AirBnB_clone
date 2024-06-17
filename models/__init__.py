#!/usr/bin/python3
"""Create a unique FileStorage instance for your application"""
from models.engine.file_storage import FileStorage
from models.user import User


storage = FileStorage()
storage.reload()
