#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError, NoResultFound
from sqlalchemy.orm import sessionmaker, scoped_session
from user import Base, User


class DB:
    """DB class to manage database operations"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = scoped_session(sessionmaker(bind=self._engine))

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
        session = self.__session()
        session.add(new_user)
        session.commit()
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
        session = self.__session()
        try:
            return session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound(f"No user found with criteria: {kwargs}")
        except InvalidRequestError:
            raise InvalidRequestError(f"Invalid query arguments: {kwargs}")

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
        session = self.__session()
        user = self.find_user_by(id=user_id)

        # Get all valid attributes from the User model
        valid_attributes = User.__table__.columns.keys()

        for key, value in kwargs.items():
            if key not in valid_attributes:
                raise ValueError(
                    f"Invalid attribute '{key}'. "
                    f"Valid attributes: {valid_attributes}"
                )
            setattr(user, key, value)

        session.commit()
