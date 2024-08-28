#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """Create user table in the database"""
    if models.storage_type == "db":
        __tablename__ = 'users'
        username = Column(String(45), nullable=False)
        email = Column(String(45), nullable=False)
        password_hash = Column(String(60), nullable=False)
