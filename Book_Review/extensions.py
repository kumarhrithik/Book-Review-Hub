from flask_pymongo import PyMongo
from flask_principal import Principal
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

mongo = PyMongo()
bcrypt = Bcrypt()
principals = Principal()
login_manager = LoginManager()
