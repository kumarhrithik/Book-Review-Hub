from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from bson import ObjectId
from ..extensions import mongo
from ..models import Book, Review, Comment

books = Blueprint('books', __name__)

@books.route('/add_book', methods=['POST'])
@login_required
def add_book():
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
    data = request.json
    book = Book.objects.get_or_404(id=ObjectId(book_id))
    review = Review(rating=data.get('rating'), text=data.get('text'), user_id=current_user.id, book_id=book.id)
    review.save()
    return jsonify({'message': 'Review posted successfully'})

@books.route('/reviews/<string:review_id>', methods=['PUT', 'DELETE'])
@login_required
def edit_or_delete_review(review_id):
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
    data = request.json
    review = Review.objects.get_or_404(id=ObjectId(review_id))
    comment = Comment(text=data.get('text'), user_id=current_user.id, review_id=review.id)
    comment.save()
    return jsonify({'message': 'Comment posted successfully'})

@books.route('/edit_comment/<string:comment_id>', methods=['PUT'])
@login_required
def edit_comment(comment_id):
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
    comment = Comment.objects.get_or_404(id=ObjectId(comment_id), user_id=current_user.id)

    # Check if the user deleting the comment is the owner
    if current_user.id == comment.user_id:
        comment.delete()
        return jsonify({'message': 'Comment deleted successfully'})
    else:
        return jsonify({'error': 'Unauthorized to delete this comment'}), 403

@books.route('/filter_books', methods=['GET'])
def filter_books():
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
