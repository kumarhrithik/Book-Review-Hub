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
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized to access this resource'}), 403

    users = User.objects()
    users_data = [{'username': user.username, 'role': user.role} for user in users]
    return jsonify(users_data)

@admin.route('/moderate_reviews', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def moderate_reviews():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized to access this resource'}), 403

    reviews = Review.objects()
    reviews_data = [{'user': review.user.username, 'book': review.book.title, 'rating': review.rating, 'text': review.text} for review in reviews]
    return jsonify(reviews_data)

@admin.route('/moderate_comments', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def moderate_comments():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized to access this resource'}), 403

    comments = Comment.objects()
    comments_data = [{'user': comment.user.username, 'review': comment.review.id, 'text': comment.text} for comment in comments]
    return jsonify(comments_data)

