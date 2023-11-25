"""
Module for defining data models used in the Book Review Platform API.

This module includes the definition of User, Task, Book, Review, and Comment models using Flask-MongoEngine.
"""

from flask_pymongo import PyMongo
from flask_login import UserMixin

mongo = PyMongo()

class User(UserMixin, mongo.Document):
    """
    User model class representing a user in the system.

    Attributes:
        username (str): User's username.
        password (str): User's password (hashed).
        role (str): User's role, defaults to 'user'.
    """
    username = mongo.StringField(required=True, unique=True)
    password = mongo.StringField(required=True)
    role = mongo.StringField(default='user')

class Task(mongo.Document):
    """
    Task model class representing a task in the system.

    Attributes:
        title (str): Task title.
        description (str): Task description.
        completed (bool): Task completion status.
        user_id (ObjectId): User ID associated with the task.
    """
    title = mongo.StringField(required=True)
    description = mongo.StringField()
    completed = mongo.BooleanField(default=False)
    user_id = mongo.ObjectIdField()

class Book(mongo.Document):
    """
    Book model class representing a book in the system.

    Attributes:
        title (str): Book title.
        author (str): Book author.
        genre (str): Book genre.
        publication_year (int): Book publication year.
    """
    title = mongo.StringField(required=True)
    author = mongo.StringField(required=True)
    genre = mongo.StringField(required=True)
    publication_year = mongo.IntField(required=True)

class Review(mongo.Document):
    """
    Review model class representing a review for a book.

    Attributes:
        rating (int): Review rating.
        text (str): Review text.
        user_id (ObjectId): User ID associated with the review.
        book_id (ObjectId): Book ID associated with the review.

    """
    rating = mongo.IntField(required=True)
    text = mongo.StringField()
    user_id = mongo.ObjectIdField()
    book_id = mongo.ObjectIdField()

class Comment(mongo.Document):
    """
    Comment model class representing a comment on a review.

    Attributes:
        text (str): Comment text.
        user_id (ObjectId): User ID associated with the comment.
        review_id (ObjectId): Review ID associated with the comment.
    """
    text = mongo.StringField()
    user_id = mongo.ObjectIdField()
    review_id = mongo.ObjectIdField()
