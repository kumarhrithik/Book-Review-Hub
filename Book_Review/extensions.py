"""
Module for initializing Flask extensions.

This module includes initialization of PyMongo, Bcrypt, Principal, and LoginManager extensions.

Extensions:
    mongo (PyMongo):
        Flask extension for interacting with MongoDB.
        Used for database operations in the Book Review Platform API.

    bcrypt (Bcrypt):
        Flask extension for hashing passwords using the bcrypt hashing algorithm.
        Used for securely storing user passwords.

    principals (Principal):
        Flask extension for managing identity and access control.
        Used for implementing Role-Based Access Control (RBAC) in the API.

    login_manager (LoginManager):
        Flask extension for managing user sessions and authentication.
        Used for handling user authentication in the API.

"""

from flask_pymongo import PyMongo
from flask_principal import Principal
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

mongo = PyMongo()
bcrypt = Bcrypt()
principals = Principal()
login_manager = LoginManager()
