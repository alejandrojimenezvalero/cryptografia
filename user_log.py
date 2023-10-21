"""This module allows us to manage the user log"""
from db_connection import dbConnection


class User:

    def __init__(self, option):
        self._con = dbConnection(option)
        self._email = None
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
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def usingForum(self):
        return self._usingForum

    @usingForum.setter
    def usingForum(self, forum_name):
        self._usingForum = forum_name
