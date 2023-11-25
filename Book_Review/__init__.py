"""
Module for creating the Flask application and initializing extensions.

This module initializes the Flask application and configures various extensions such as PyMongo, Bcrypt, 
Principal, and LoginManager. It also registers the blueprints for different routes.
"""

from flask import Flask
from .extensions import mongo, bcrypt, principals, login_manager
import os
from .routes import tasks, auth, admin, books

def create_app():
    
    """
    Function to create and configure the Flask application.

    Returns:
        Flask: Configured Flask application.
    """

    app = Flask(__name__)
    app.config['MONGO_URI'] = " " #Database URI Reference Used For is MondoDB  
    app.secret_key = os.urandom(32)

    mongo.init_app(app)
    bcrypt.init_app(app)
    principals.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(tasks)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(books)

    return app

