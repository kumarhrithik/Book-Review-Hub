# LitRate: The Book Review Hub

LitRate is a RESTful API for a Book Review Platform built using Flask. The platform allows users to post book reviews, rate books, and comment on reviews. It includes user authentication, role-based access control, and advanced functionalities like search and filtering.

## Project Structure


## Setup Instructions

Documentation and Testing
To set up and test the LitRate API, follow these steps:

1. Clone the repository: git clone [repository-url]
2. Install dependencies: pip install -r requirements.txt
3. Set up a MongoDB database and update the MONGO_URI in __init__.py.
4. Run the application: python run.py
5. Access the API documentation at http://localhost:5000/docs.

Certainly! Below is a comprehensive documentation for all the endpoints in your Flask API:

## API Documentation

### Authentication

#### Login

- **Endpoint:** `/login`
  - **Method:** `POST`
  - **Request Body:**
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
  - **Response:**
    ```json
    {
      "message": "Login successful",
      "access_token": "your_access_token"
    }
    ```

#### Register

- **Endpoint:** `/register`
  - **Method:** `POST`
  - **Request Body:**
    ```json
    {
      "username": "new_username",
      "password": "new_password"
    }
    ```
  - **Response:**
    ```json
    {
      "message": "User registered successfully"
    }
    ```

### Books

#### Add Book

- **Endpoint:** `/add_book`
  - **Method:** `POST`
  - **Request Body:**
    ```json
    {
      "title": "Book Title",
      "author": "Author Name",
      "genre": "Genre",
      "publication_year": 2022
    }
    ```
  - **Response:**
    ```json
    {
      "message": "Book added successfully"
    }
    ```

#### Post Review

- **Endpoint:** `/post_review/{book_id}`
  - **Method:** `POST`
  - **Request Body:**
    ```json
    {
      "rating": 4,
      "text": "Great book!"
    }
    ```
  - **Response:**
    ```json
    {
      "message": "Review posted successfully"
    }
    ```

#### Edit or Delete Review

- **Endpoint:** `/reviews/{review_id}`
  - **Methods:** `PUT`, `DELETE`
  - **Request Body (PUT):**
    ```json
    {
      "rating": 5,
      "text": "Absolutely amazing!"
    }
    ```
  - **Response (PUT):**
    ```json
    {
      "message": "Review edited successfully"
    }
  - **Response (DELETE):**
    ```json
    {
      "message": "Review deleted successfully"
    }
    ```

#### Post Comment

- **Endpoint:** `/post_comment/{review_id}`
  - **Method:** `POST`
  - **Request Body:**
    ```json
    {
      "text": "Insightful comment!"
    }
    ```
  - **Response:**
    ```json
    {
      "message": "Comment posted successfully"
    }
    ```

#### Edit Comment

- **Endpoint:** `/edit_comment/{comment_id}`
  - **Method:** `PUT`
  - **Request Body:**
    ```json
    {
      "text": "Updated insightful comment!"
    }
    ```
  - **Response:**
    ```json
    {
      "message": "Comment edited successfully"
    }
    ```

#### Delete Comment

- **Endpoint:** `/delete_comment/{comment_id}`
  - **Method:** `DELETE`
  - **Response:**
    ```json
    {
      "message": "Comment deleted successfully"
    }
    ```

#### Filter Books

- **Endpoint:** `/filter_books`
  - **Method:** `GET`
  - **Query Parameters:**
    - `rating` (optional): Filter by book rating (1-5).
    - `publication_year` (optional): Filter by publication year.
  - **Response:**
    ```json
    [
      {
        "title": "Book Title",
        "author": "Author Name",
        "genre": "Genre",
        "publication_year": 2022
      },
      ...
    ]
    ```

### Admin

#### Manage Users

- **Endpoint:** `/manage_users`
  - **Method:** `GET`
  - **Requires:** Administrator role
  - **Response:**
    ```json
    [
      {
        "username": "user1",
        "role": "user"
      },
      {
        "username": "admin1",
        "role": "admin"
      },
      ...
    ]
    ```

#### Moderate Reviews

- **Endpoint:** `/moderate_reviews`
  - **Method:** `GET`
  - **Requires:** Administrator role
  - **Response:**
    ```json
    [
      {
        "user": "user1",
        "book": "Book Title",
        "rating": 4,
        "text": "Great book!"
      },
      ...
    ]
    ```

#### Moderate Comments

- **Endpoint:** `/moderate_comments`
  - **Method:** `GET`
  - **Requires:** Administrator role
  - **Response:**
    ```json
    [
      {
        "user": "user1",
        "review": "review_id",
        "text": "Insightful comment!"
      },
      ...
    ]
    ```

This documentation provides a detailed guide on using each endpoint along with the required parameters and expected responses. Ensure that your API follows the documented conventions. You may also consider using tools like Swagger for interactive documentation.


Note: Ensure that you have MongoDB installed and running before starting the application.