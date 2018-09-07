from flask_restful import Resource
from flask import request, jsonify
from app.book.models import Book, BorrowedBook
from app.user.models import User
from utils.json_schema import login_required, admin_required

class Users(Resource):
    @classmethod
    @admin_required
    def get(self, userid=None):
        if userid != None:
            this_user = User.get_by_id(userid)
            if not this_user:
                return 'User not found', 404
            return ({'user': {'Id': this_user.id, 'username': this_user.username, 'email': this_user.email,
                              'role': this_user.role}},
                    {'message': 'Gets a specific user'}), 200
        else:
            return User.get_many()


class Borrow(Resource):
    @login_required
    def post(current_user, self, bookid=None):
        book_instance = Book.query.filter_by(book_id=bookid).first()
        if not book_instance:
            return {"error": "Book not found"}, 404
        # check if book is borrowed
        if not book_instance.available:
            return {"message": "Book unavailable, please try later"}, 400
        borrowed_book_instance = BorrowedBook.query.filter_by(book_id=bookid,return_status='false').first()
        if borrowed_book_instance:
            return {"error": "book already borrowed"}, 401
        this_user = current_user.id
        BorrowedBook(this_user, book_instance.book_id).save()
        return {"message": "Borrow Success"}, 200


class Return(Resource):
    @login_required
    def put(current_user, self, book_id=None):
        book_instance = BorrowedBook.query.filter_by(book_id=book_id).first()
        if not book_instance:
            return {"error": "book not found"}, 404
        # check if book is borrowed
        if book_instance.return_status:
            return {"message": "Book has already been returned"}, 400

        if not current_user:
            return 'User details missing', 401
        book_instance.return_book()
        return {"message": "Return Success"}, 200

class MyBorrowed(Resource):
    @login_required
    def get(current_user, self, book_id=None):
        this_user = current_user.id
        # if action === "borrowed":
        #     book_instance = BorrowedBook.query.filter_by(user_id=this_user, return_status="true").first()
        # else if action === "returned":
        #     book_instance = BorrowedBook.query.filter_by(user_id=this_user, return_status="true").first()
        # else:
        #     book_instance = BorrowedBook.query.filter_by(user_id=this_user).first()
        book_instance = BorrowedBook.query.filter_by(user_id=this_user).first()
        if not book_instance:
            return {"error": "Book not found"}, 404
        # check if book is borrowed
        if not book_instance.book_id:
            return {"message": "This book is an incorect entry"}, 400
        #BorrowedBook(this_user, book_instance.book_id).save()
        # const items = [
        #     'foo',
        #     ... true ? ['bar'] : [],
        #     ... false ? ['falsy'] : [],
        #     ]
        #action = request.args.get('theaction', default=False, type=bool)
        search_vars = {
            'page': request.args.get('page', 1, type=int),
            'isbn': request.args.get('isbn', None, type=str),
            'author': request.args.get('author', default=None, type=str),
            'title': request.args.get('title', None, type=str),
            'copies': request.args.get('copies', "10", type=str),
            'user_id': request.args.get('user_id', default=this_user, type=str),
            'return_status': request.args.get('theaction', default=False, type=bool),
            'history': request.args.get('history', default=False, type=bool),
            'limit': request.args.get('limit', 20, type=int)
        }
        results = BorrowedBook.search(search_vars)
        itemized = results.items
        # json.dumps(my_dictionary, indent=4, sort_keys=True, default=str)
        return {
            "page": results.page,
            "total_results": results.total,
            "total_pages": results.pages,
            "per_page": results.per_page,
            "objects": [{'book_id': Book.book_id, 'user_id': Book.user_id,
                         'borrow_date': str(Book.borrow_date), 'return_date': str(Book.return_date),
                         'status': Book.return_status, 'log': Book.borrow_id
                         } for Book in itemized
                        ],
            "message":"View borrowed books Success"}, 200
        # return {"message": 
