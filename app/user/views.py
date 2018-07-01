from flask_restful import Resource
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
        #req_data = request.get_json()
        #this_user = req_data["user_id"]
        book_instance.return_book()
        return {"message": "Return Success"}, 200

