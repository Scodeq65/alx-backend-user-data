#!/usr/bin/env python3
"""
This module defines the SQLAlchemy model for the `users` table.
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

# Base class for our SQLAlchemy models
Base = declarative_base()


class User(Base):
    """
    User model for the `users` table.

    Attributes:
        id (int): Primary key, unique identifier for
        each user.
        email (str): Non-nullable string representing the
        user's email.
        hashed_password (str): Non-nullable string for
        storing hashed passwords.
        session_id (str): Nullable string for session ID.
        reset_token (str): Nullable string for reset token.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
