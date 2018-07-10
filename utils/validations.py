import re
from app.user.models import User
from app.book.models import Book, BorrowedBook


def validate_field(field, value, error):
    """validates if username is already taken"""
    value = value.strip().lower()
    tables = {"username": User, "name": Book}
    queries = {}
    if field == "username":
        queries[field] = [User.username.ilike(value)]
    else:
        queries[field] = [Book.name.ilike(value)]
    if not value:
        error(field, "Field cannot be empty")
    error(field, "Sorry!! %s taken!" % (field)) if tables[field].query.filter(*queries[field]).first() else ""


def validate_email(field, value, error):
    """Check that the email is in the correct format"""
    email = value.strip().lower()
    if not email:
        error(field, "Field cannot be empty")
    User.get_by_email(email)
    if User.get_by_email(email):
        error(field, "Sorry!! Email taken!")
    if not re.match(
            r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,4}$', value):
        error(field, "Invalid Email")


def username_taken(field, value, error):
    """Checks if the provided username exists"""
    username = value.strip().lower()
    if not username:
        error(field, "Field cannot be empty")
    User.get_by_username(username)
    # if not User.query.filter_by(username=username).first():
    #     error(field, "Sorry!! Username not found!")


def validate_password(field, value, error):
    """Ensures passwords are long enough and checks the range of values is allowed"""
    if not re.match(r'\A[0-9a-zA-Z!@#$%&*]{6,20}\Z', value):
        error(
            field,
            "Password must be 6-20 Characters and can only contains letters,numbers,and any of !@#$%"
        )
