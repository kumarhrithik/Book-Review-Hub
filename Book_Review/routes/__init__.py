from flask import Blueprint

tasks = Blueprint('tasks', __name__)
auth = Blueprint('auth', __name__)
admin = Blueprint('admin', __name__)
books = Blueprint('books', __name__)

from . import tasks, auth, admin, books
