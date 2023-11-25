"""
Module for admin-related routes and functionalities.

This module includes routes for managing users, moderating reviews, and moderating comments.
"""

from flask import Blueprint, jsonify
from flask_principal import Permission
from flask_login import login_required, current_user
from ..models import User, Review, Comment
from ..extensions import principals

admin = Blueprint('admin', __name__)

admin_permission = Permission(principals.RoleNeed('admin'))


@admin.route('/manage_users', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def manage_users():
    """
    Endpoint for administrators to retrieve a list of all users and their roles.

    Method:
        GET

    Request Headers:
        Authorization: Bearer <access_token>

    Returns:
        json: A JSON object containing user data, including usernames and roles.
    """


    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized to access this resource'}), 403

    users = User.objects()
    users_data = [{'username': user.username, 'role': user.role} for user in users]
    return jsonify(users_data)

@admin.route('/moderate_reviews', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def moderate_reviews():
    """
    Endpoint for administrators to retrieve a list of all book reviews with user details.

    Method:
        GET

    Request Headers:
        Authorization: Bearer <access_token>

    Returns:
        json: A JSON object containing review data, including usernames, book titles, ratings, and review text.
    """

    
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized to access this resource'}), 403

    reviews = Review.objects()
    reviews_data = [{'user': review.user.username, 'book': review.book.title, 'rating': review.rating, 'text': review.text} for review in reviews]
    return jsonify(reviews_data)

@admin.route('/moderate_comments', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def moderate_comments():
    """
    Endpoint for administrators to retrieve a list of all comments on book reviews.

    Method:
        GET

    Request Headers:
        Authorization: Bearer <access_token>

    Returns:
        json: A JSON object containing comment data, including usernames, review IDs, and comment text.
    """

    
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized to access this resource'}), 403

    comments = Comment.objects()
    comments_data = [{'user': comment.user.username, 'review': comment.review.id, 'text': comment.text} for comment in comments]
    return jsonify(comments_data)

