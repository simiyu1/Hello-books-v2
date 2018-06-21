from flask_restful import Resource
from flask import request

#from app.bookdir.views import books_list
from app.userdir.models import User
from app.bookdir.models import Book

# # Create dummy users dataset to hold dummy users
# users_list = []
# user1 = User(1,'Mainmuna Swazi','pass123')
# user2 = User(2,'Mwenda Kifikifi','pass123')
# user3 = User(3,'Khololosia Mbi','pass123')
# user4 = User(4,'Kinde Kinde','pass123')
# user4.isadmin = True
# user4.active = True
# user5 = User(5,'Miguna','pass123')
# user5.active = True
# users_list.append(user2)
# users_list.append(user3)
# users_list.append(user4)
# users_list.append(user5)
# borrowed_books = []
# book1 = Book(1,'The Eleventh Commandment','Jeffrey Archer')
# book2 = Book(2,'If Tomorrow Comes','Sidney Sheldon')
# user1.borrowed_books.append(book1)
# user1.borrowed_books.append(book2)
# users_list.append(user1)


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

class Borrow(Resource):
    @classmethod
    def post(self, ISBN=None):
        req_data = request.get_json()
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
                return (borrowed, {'message': 'book borrowed'}), 200