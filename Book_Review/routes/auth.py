from flask import Blueprint, request, jsonify
from flask_login import login_user
from ..extensions import bcrypt, mongo
from ..models import User

auth = Blueprint('auth', __name__)

from flask_jwt_extended import create_access_token

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.objects(username=data['username']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'message': 'Login successful', 'access_token': access_token})
    return jsonify({'message': 'Invalid credentials'})


@auth.route('/register', methods=['POST'])
def register():
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