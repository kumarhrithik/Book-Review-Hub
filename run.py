"""
Module for running the Flask application.

This module creates and runs the Flask app using the create_app function from the Book_Review package.
"""

from Book_Review import create_app 

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
