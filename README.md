# Hello-Booksv2
[![Build Status](https://travis-ci.org/simiyu1/Hello-books-v2.svg?branch=ch-badges)](https://travis-ci.org/simiyu1/Hello-books-v2)
[![Coverage Status](https://coveralls.io/repos/github/simiyu1/Hello-books-v2/badge.svg)](https://coveralls.io/github/simiyu1/Hello-books-v2)
[![Build Status](https://travis-ci.org/simiyu1/Hello-books-v2.svg?branch=develop)](https://travis-ci.org/simiyu1/Hello-books-v2)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ec6ae08c817d4307a343b67ac4090dda)](https://www.codacy.com/app/simiyu1/Hello-books-v2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=simiyu1/Hello-books-v2&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/9fa648d0b3562db54173/maintainability)](https://codeclimate.com/github/simiyu1/Hello-books-v2/maintainability)

This is a python based API that helps to keeps track of library transactions and records. It will allow services to connect to the endpoints and register or login users, borrow books, and allow privileged users to add or edit book information.

# Specifications

| EndPoint | Functionality | Access Rights |
| ------------- | ------------- | ------------- |
| PUT /api/books/<bookId> |modify a book’s information  | Admin only |
|DELETE /api/books/<bookId> | Remove a book  | Admin only |
| GET /api/books | Retrieves all books | Logged in users only |
| GET /api/books/<bookId> | Get a book | Logged in users only |
| POST /api/users/books/<bookId> | Borrow a book  | Logged in users only |
| POST /api/auth/register | Creates a user account | Any one |
| POST /api/auth/login | Logs in a user | Logged in users only |
| POST /api/auth/logout | Logs out a user | Logged in users only |
| POST /api/auth/reset-password | Password reset | Logged in users only |
|  |  |


# Installation


   i. Clone or download the repository
      `git clone https://github.com/simiyu1/Hello-Booksv2/develop/`

   ii. Create a virtual environment
      `virtualenv venv`
      In windows `mkvirtualenv venv`

   iii. Activate the environment 
      `source venv\bin\activate`
      in windows use `venv/Scripts/activate`

   iv. Install the environmmental requirements from the file within the virtual venv
       `pip install -r requirements.txt`

## Running the tests
        `python -m unittest discover -v` (Runs all tests in windows)
       or using nosetests
         `nosetests --with-coverage --cover-package=app`

## Running the API
    i. Cd into the directory "Hello-Booksv2" the run the command
        `python run.py`
        In your terminal

# Documentation
Find a detailed documentation on the expected data types, and anticipated responce data from this Apiary link https://hello332.docs.apiary.io

# Contribution
The nature of this project does not allow contributions. However, comments on my pull requests are welcome, you are also free to clone this repo and build from it. :-)