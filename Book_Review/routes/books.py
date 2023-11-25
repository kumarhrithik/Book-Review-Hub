"""
Module for book-related routes and functionalities.

This module includes routes for adding books, posting reviews, editing and deleting reviews and comments, 
posting comments, and filtering books.
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId
from ..extensions import mongo
from ..models import Book, Review, Comment

books = Blueprint('books', __name__)

@books.route('/add_book', methods=['POST'])
@login_required
def add_book():
    """
    Endpoint for users to add a new book to the platform.

    Method: POST
    Route: '/add_book'
    Request Format:
        {
            "title": "string",
            "author": "string",
            "genre": "string",
            "publication_year": integer
        }
    Response Format:
        {
            "message": "Book added successfully"
        }
    """
    data = request.json
    try:
        publication_year = int(data.get('publication_year'))
    except ValueError:
        return jsonify({'error': 'Invalid publication year'}), 400

    book = Book(title=data.get('title'), author=data.get('author'), genre=data.get('genre'), publication_year=publication_year)
    book.save()
    return jsonify({'message': 'Book added successfully'})

@books.route('/post_review/<string:book_id>', methods=['POST'])
@login_required
def post_review(book_id):
    """
    Endpoint for users to post a review for a specific book.

    Method: POST
    Route: '/post_review/<string:book_id>'
    Request Format:
        {
            "rating": integer (1-5),
            "text": "string"
        }
    Response Format:
        {
            "message": "Review posted successfully"
        }
    """
    data = request.json
    book = Book.objects.get_or_404(id=ObjectId(book_id))
    review = Review(rating=data.get('rating'), text=data.get('text'), user_id=current_user.id, book_id=book.id)
    review.save()
    return jsonify({'message': 'Review posted successfully'})

@books.route('/reviews/<string:review_id>', methods=['PUT', 'DELETE'])
@login_required
def edit_or_delete_review(review_id):
    """
    Endpoint for users to edit or delete their own reviews.

    Methods: 
        - PUT (Edit)
        - DELETE (Delete)
    Route: '/reviews/<string:review_id>'
    Request Format (for edit):
        {
            "rating": integer (1-5),
            "text": "string"
        }
    Response Format (for edit):
        {
            "message": "Review edited successfully"
        }
    Response Format (for delete):
        {
            "message": "Review deleted successfully"
        }
    """
    data = request.json
    review = Review.objects.filter(id=ObjectId(review_id), user_id=current_user.id).first()

    if not review:
        return jsonify({'error': 'Review not found or unauthorized to edit/delete'}), 404

    if request.method == 'PUT':
        if current_user.id == review.user_id:
            review.update(**data)
            return jsonify({'message': 'Review edited successfully'})
        else:
            return jsonify({'error': 'Unauthorized to edit this review'}), 403
    elif request.method == 'DELETE':
        # Check if the user deleting the review is the owner
        if current_user.id == review.user_id:
            review.delete()
            return jsonify({'message': 'Review deleted successfully'})
        else:
            return jsonify({'error': 'Unauthorized to delete this review'}), 403


@books.route('/post_comment/<string:review_id>', methods=['POST'])
@login_required
def post_comment(review_id):
    """
    Endpoint for users to post a comment on a review.

    Method: POST
    Route: '/post_comment/<string:review_id>'
    Request Format:
        {
            "text": "string"
        }
    Response Format:
        {
            "message": "Comment posted successfully"
        }
    """
    data = request.json
    review = Review.objects.get_or_404(id=ObjectId(review_id))
    comment = Comment(text=data.get('text'), user_id=current_user.id, review_id=review.id)
    comment.save()
    return jsonify({'message': 'Comment posted successfully'})

@books.route('/edit_comment/<string:comment_id>', methods=['PUT'])
@login_required
def edit_comment(comment_id):
    """
    Endpoint for users to edit their own comments.

    Method: PUT
    Route: '/edit_comment/<string:comment_id>'
    Request Format:
        {
            "text": "string"
        }
    Response Format:
        {
            "message": "Comment edited successfully"
        }

    """
    data = request.json
    comment = Comment.objects.get_or_404(id=ObjectId(comment_id), user_id=current_user.id)

    # Check if the user editing the comment is the owner
    if current_user.id == comment.user_id:
        comment.update(**data)
        return jsonify({'message': 'Comment edited successfully'})
    else:
        return jsonify({'error': 'Unauthorized to edit this comment'}), 403

@books.route('/delete_comment/<string:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    """
    Endpoint for users to delete their own comments.

    Method: DELETE
    Route: '/delete_comment/<string:comment_id>'
    Response Format:
        {
            "message": "Comment deleted successfully"
        }
    """
    comment = Comment.objects.get_or_404(id=ObjectId(comment_id), user_id=current_user.id)

    # Check if the user deleting the comment is the owner
    if current_user.id == comment.user_id:
        comment.delete()
        return jsonify({'message': 'Comment deleted successfully'})
    else:
        return jsonify({'error': 'Unauthorized to delete this comment'}), 403

@books.route('/filter_books', methods=['GET'])
def filter_books():
    """
    Endpoint for filtering books based on specified parameters.

    Method: GET
    Route: '/filter_books'
    Query Parameters (Optional):
        - rating: integer (1-5)
        - publication_year: integer
    Response Format:
        [
            {
                "title": "string",
                "author": "string",
                "genre": "string",
                "publication_year": integer
            },
            ...
        ]
    """
    rating = request.args.get('rating')
    publication_year = request.args.get('publication_year')

    query_params = {}

    if rating:
        query_params['rating'] = int(rating)

    if publication_year:
        query_params['publication_year'] = int(publication_year)

    books = Book.objects(**query_params)
    books_data = [{'title': book.title, 'author': book.author, 'genre': book.genre, 'publication_year': book.publication_year} for book in books]
    return jsonify(books_data)
