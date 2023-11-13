from flask_pymongo import PyMongo
from flask_login import UserMixin

mongo = PyMongo()

class User(UserMixin, mongo.Document):
    username = mongo.StringField(required=True, unique=True)
    password = mongo.StringField(required=True)
    role = mongo.StringField(default='user')

class Task(mongo.Document):
    title = mongo.StringField(required=True)
    description = mongo.StringField()
    completed = mongo.BooleanField(default=False)
    user_id = mongo.ObjectIdField()

class Book(mongo.Document):
    title = mongo.StringField(required=True)
    author = mongo.StringField(required=True)
    genre = mongo.StringField(required=True)
    publication_year = mongo.IntField(required=True)

class Review(mongo.Document):
    rating = mongo.IntField(required=True)
    text = mongo.StringField()
    user_id = mongo.ObjectIdField()
    book_id = mongo.ObjectIdField()

class Comment(mongo.Document):
    text = mongo.StringField()
    user_id = mongo.ObjectIdField()
    review_id = mongo.ObjectIdField()
