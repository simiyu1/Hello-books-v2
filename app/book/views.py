from flask_restful import Resource
from flask import request, jsonify
from app.book.models import Book
from app.user.models import User
from utils.json_schema import login_required, admin_required

class books(Resource):
    @classmethod
    def get(cls, bookid=None):
        if bookid != None:
            book_to_find = Book.get_by_id(bookid)
            if not book_to_find:
                return {'message': 'Item not found'}, 404
            return {'ISBN': book_to_find.isbn, 'title': book_to_find.title, 'book_id': book_to_find.book_id, 'Copies': book_to_find.copies,'author': book_to_find.author, 'message': 'Gets a specific book'}, 200
        else:
            return Book.get_many(), 200

    @classmethod
    def make_response(self, Book):
        data = {'ISBN': Book.ISBN, 'title': Book.title, 'author': Book.author}
        return data, 200

    @staticmethod
    @admin_required
    @login_required
    def post(current_user):
        req_data = request.get_json()
        if not req_data['author']:
            return {'message': 'missing book details'}, 404
        ISBN = req_data['ISBN']
        title = req_data['title']
        author = req_data['author']
        copies = req_data['copies']

        isbn_exists = Book.get_by_isbn(ISBN)
        if not isbn_exists:
            Book(ISBN=ISBN, title=title, author=author, copies=copies).save()
            return {"message": "book added"}, 200
        else:
            return {"message": "Failed, Book exists"}, 400

    @staticmethod
    @admin_required
    @login_required
    def delete(current_user, bookid=None):
        if bookid is None:
            return {"message": "book ID expected"}, 406
        book_to_delete = Book.get_by_id(bookid)
        if not book_to_delete:
            return {'message': 'book entry not found'}, 400
        else:
            book_to_delete.book_delete()
            return {"message": "Success, Book deleted"}, 200

    @staticmethod
    @admin_required
    @login_required
    def put(current_user, bookid=None):
        if bookid is None:
            return {"message": "book id required"}, 406
        req_data = request.get_json()
        book_to_update = Book.get_by_id(bookid)
        if not book_to_update:
            return {"message": "book to update not found"}, 401
        if not req_data:
            return {"message": "book details missing"}, 406
        prev_isbn = book_to_update.isbn
        prev_title = book_to_update.title
        prev_author = book_to_update.author
        prev_copies = book_to_update.copies
        prev_available = book_to_update.available
        if 'ISBN' in req_data:
            isbn = req_data['ISBN']
        else:
            isbn = prev_isbn
        if 'title' in req_data:
            title = req_data['title']
        else:
            title = prev_title
        if 'author' in req_data:
            author = req_data['author']
        else:
            author = prev_author
        if 'available' in req_data:
            available = req_data['available']
        else:
            available = prev_available
        if 'copies' in req_data:
            copies = req_data['copies']
        else:
            copies = prev_copies

        book_to_update.update(isbn, author, title, copies, available)
        return {"message": "Success, Book updated"}, 200
