#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class to manage database operations"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)  # Add the new user to the session
        self._session.commit()  # Commit the session to save changes
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the query.

        Returns:
            User: The first User object that matches the filter.

        Raises:
            InvalidRequestError: If the query contains invalid arguments.
            NoResultFound: If no user is found for the given filter.
        """
        try:
            # Query the User model with the provided filter
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found for the given criteria")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Key-value pairs of attributes to update.

        Returns:
            None

        Raises:
            ValueError: If an argument does not correspond to a
            valid user attribute.
        """
        # Locate the user
        user = self.find_user_by(id=user_id)

        # Update the user's attributes
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(
                    f"Attribute {key} does not exist on the User model"
                )
            setattr(user, key, value)

        # Commit the changes
        self._session.commit()
