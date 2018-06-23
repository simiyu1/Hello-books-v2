from flask_restful import Resource
from flask import request


#from app.bookdir.views import books_list
#from app.userdir.models import User
from app.bookdir.models import Book, BorrowedBook
from app.auth.helper import token_required

class Users(Resource):
    @classmethod
    def get(self, userid=None):
        if request.args.get('userid') != None:
            received_ID = request.args.get('userid')
            empty_users_list=[]
            items = []
            items = [user for user in users_list if user.userid == int(received_ID)]
            if (int(received_ID)==3):
                items = [user for user in empty_users_list if user.userid == int(received_ID)]
            if len(items) < 1:

                return 'User not found', 404
            return ({'user':{'userid': items[0].userid, 'username': items[0].username, 'logged in': items[0].active}}, {'message': 'Fetched User'}), 200
        else:
            items = []
            if len(users_list) < 1:
                return 'Users not found', 404
            for user in users_list:
                items.append({'userid': user.userid, 'username': user.username, 'logged in':user.active})
            return (items,
                     {'message': 'fetched User'}), 200


#@token_required
class Borrow(Resource):
    @token_required
    def post(self, bookid=None):
        book_instance = Book.query.filter_by(book_id=bookid).first()
        if not book_instance:
            return {"error": "book not found"}, 404
        # check if book is borrowed
        if not book_instance.available:
            return {"message": "Book unavailable, please try later"}, 400

        if not request.get_json():
            return 'User details missing',401
        req_data = request.get_json()
        this_user = req_data["user_id"]
        BorrowedBook(this_user, book_instance.book_id).save()
        return {"message": "Borrow Success"}, 200


class Return(Resource):
    @classmethod
    def put(self, book_id=None):
        book_instance = BorrowedBook.query.filter_by(book_id=book_id).first()
        if not book_instance:
            return {"error": "book not found"}, 404
        # check if book is borrowed
        if book_instance.return_status:
            return {"message": "Book has already been returned"}, 400

        if not request.get_json():
            return 'User details missing', 401
        #req_data = request.get_json()
        #this_user = req_data["user_id"]
        book_instance.return_book()
        return {"message": "Return Success"}, 200


""""req_data = request.get_json()
        if not request.get_json():
            return 'User details missing',401
        recieved_ISBN = ISBN
        user_id = req_data['userid']
        exists = [
            user for user in users_list if user.userid == user_id and user.active==True]
        if not exists:
            return {"message":"Not logged in"}, 406
        borrowed = []
        if len(books_list) < 1: #Chec if there are books in the library
            return {"message":"no Books in the library"}, 404
        else:
            item_id = recieved_ISBN
            book = [item for item in books_list if item.ISBN == int(item_id) ]
            if not book:
                return {"message": "no book found with the given book id"}, 404
            else:
                borrowed = book[0].title
                return (borrowed, {'message': 'book borrowed'}), 200"""
