from flask_restful import Resource
from flask import request
from app.bookdir.models import Book


# #Dummy dataset to hold all books in the app
# books_list = []
# book1 = Book(1,'The Eleventh Commandment','Jeffrey Archer')
# book2 = Book(2,'If Tomorrow Comes','Sidney Sheldon')
# book3 = Book(3,'Origin','Dan Brown')
# book4 = Book(4,'Memory Man','David Baldacci')
# book5 = Book(5,'A time to kill','John Grisham')
# book6 = Book(6,'The Pillars of the Earth','Ken Follet')
# book7 = Book(7,'Done Deal','Ken Follet')
# book8 = Book(8,'The outlet and Gober','Ken Follet')
# books_list.append(book1)
# books_list.append(book2)
# books_list.append(book3)
# books_list.append(book4)
# books_list.append(book5)
# books_list.append(book6)
# books_list.append(book7)
# books_list.append(book8)

class books(Resource):
    @classmethod
    def get(cls, isbn=None):
        #return {"Hapa   ndio" : isbn}
        print(isbn)
        #isbn = request.args['isbn']
        print(isbn)
        if isbn != None:
            book_to_find = Book.get_by_isbn(isbn)
            if not book_to_find:
                return {'message': 'Item not found'}, 404
            return ({'book': {'ISBN': book_to_find.isbn, 'title': book_to_find.title, 'author': book_to_find.author}},
                    {'message': 'Gets a specific book'}), 200
        else:
            return Book.get_many()

    @classmethod
    def make_response(self, Book):
        data = {'ISBN': Book.ISBN, 'title': Book.title, 'author': Book.author}
        return data, 200

    @classmethod
    def post(self):
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
            # return response_auth('success', 'Successfully registered', token, 201)
            # return jsonify({"Token": token})
            return {"message": "book added"}, 200
        else:
            return {"message": "Failed, Book exists"}, 400

    @classmethod
    def delete(self):
        req_data = request.get_json()
        if not req_data['ISBN']:
            return {"message": "book ID expected"}, 406
        isbn = req_data['ISBN']
        book_to_delete = Book.get_by_isbn(isbn)
        if not book_to_delete:
            return {'message': 'book entry not found'}, 400
        else:
            book_to_delete.book_delete()
            return {"message": "Success, Book deleted"}, 200

    @classmethod
    def put(self, ISBN=None):
        thisisbn = request.args['ISBN']
        if thisisbn == None:
            return {"message": "book ISBN required"}, 406
        req_data = request.get_json()
        book_to_update = Book.get_by_isbn(thisisbn)
        if not book_to_update:
            return {"message": "book to update not found"}, 401
        # if not req_data['ISBN'] or not req_data['author'] or not req_data['title'] or not req_data['copies'] or not \
        #         req_data['available']:
        #     return {"message": "book details missing"}, 406
        prev_isbn = book_to_update.isbn
        prev_title = book_to_update.title
        prev_author = book_to_update.author
        prev_copies = book_to_update.copies
        prev_available = book_to_update.available
        if req_data['ISBN']:
            isbn = req_data['ISBN']
        else:
            isbn = prev_isbn
        if req_data['title']:
            title = req_data['title']
        else:
            title = prev_title
        if req_data['author']:
            author = req_data['author']
        else:
            author = prev_author
        if req_data['available']:
            available = req_data['available']
        else:
            available = prev_available
        if req_data['copies']:
            copies = req_data['copies']
        else:
            copies = prev_copies

        book_to_update.update(isbn, author, title, copies, available)
        return {"message": "Success, Book updated"}, 200
