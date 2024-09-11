#!/usr/bin/env python3
"""
Module defining the User model for SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """
    User model for SQLAlchemy.
    Represents a user in the users table with the following attributes:
    - id: the integer primary key
    - email: a non-nullable string
    - hashed_password: a non-nullable string
    - session_id: a nullable string
    - reset_token: a nullable string
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
