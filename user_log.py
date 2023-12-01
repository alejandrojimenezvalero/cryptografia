"""This module manages the user log"""
from db_connection import dbConnection


class User:
    """This class manages all the important information of execution time related to the user"""

    def __init__(self, option):
        self._con = dbConnection(option)
        self._id = None
        self._email = None
        self._name = None
        self._second_name = None
        self._private_key = None
        self._usingForum = None
        self._cypherKeyForum = None

    @property
    def connectionDb(self):
        return self._con

    @property
    def cypherKeyForum(self):
        return self._cypherKeyForum

    @cypherKeyForum.setter
    def cypherKeyForum(self, key):
        self._cypherKeyForum = key

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def second_name(self):
        return self._second_name

    @second_name.setter
    def second_name(self, second_name):
        self._second_name = second_name

    @property
    def private_key(self):
        return self._private_key

    @private_key.setter
    def private_key(self, private_key):
        self._private_key = private_key

    @property
    def usingForum(self):
        return self._usingForum

    @usingForum.setter
    def usingForum(self, forum_name):
        self._usingForum = forum_name

    def reset_attributes(self):
        """Reset all attributes to None."""
        self._id = None
        self._email = None
        self._name = None
        self._second_name = None
        self._private_key = None
        self._usingForum = None
        self._cypherKeyForum = None
