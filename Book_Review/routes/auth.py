"""
Module for authentication routes and functionalities.

This module includes routes for user login and registration using JWT (JSON Web Tokens).

Routes:
    - '/login' (POST): Endpoint for user login.
    - '/register' (POST): Endpoint for user registration.

JWT Tokens:
    - JWT tokens are used for secure authentication.
    - Upon successful login, an access token is generated and returned to the client.
    - This access token is required for accessing protected routes.

Security Measures:
    - Passwords are securely hashed using bcrypt.
    - Proper error handling for registration and login processes.

Example Usage:
    - To log in, send a POST request to '/login' with valid credentials.
        Example: {'username': 'john_doe', 'password': 'secretpassword'}

    - To register, send a POST request to '/register' with a new username and password.
        Example: {'username': 'new_user', 'password': 'newpassword'}
"""

from flask import Blueprint, request, jsonify
from flask_login import login_user
from ..extensions import bcrypt, mongo
from ..models import User

auth = Blueprint('auth', __name__)

from flask_jwt_extended import create_access_token

@auth.route('/login', methods=['POST'])
def login():
    """
    Endpoint for user login using JWT.

    Method:
        POST

    Request Parameters:
        - username (str): User's username.
        - password (str): User's password.

    Responses:
        - 200 OK: Successful login. Returns access token.
        - 401 Unauthorized: Invalid credentials.
    """


    data = request.json
    user = User.objects(username=data['username']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'message': 'Login successful', 'access_token': access_token})
    return jsonify({'message': 'Invalid credentials'})


@auth.route('/register', methods=['POST'])
def register():
    """
    Endpoint for user registration.

    Method:
        POST

    Request Parameters:
        - username (str): User's desired username.
        - password (str): User's chosen password.

    Responses:
        - 200 OK: Successful registration. Returns a success message.
        - 400 Bad Request: Username already exists.
        - 500 Internal Server Error: Error creating user.
    """

    
    data = request.json
    existing_user = User.objects(username=data['username']).first()

    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], password=hashed_password, role='user')

    try:
        user.save()
        login_user(user)
        return jsonify({'message': 'User registered successfully'})
    except Exception as e:
        return jsonify({'error': f'Error creating user: {str(e)}'}), 500