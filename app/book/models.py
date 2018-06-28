from app import db
from datetime import datetime, timedelta
from flask import jsonify, request


class Book(db.Model):
    """Holds a book

    Attributes:
        ISBN: An integer holding a unique book number.
        title: A string holding the book title.
        author: A string holding the writer name.
        edition: A string holding the version number.
        publisher: A string holding the publishing house.
        copies: An integer holding the number of copies of the book.
        """
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(30), unique=True, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    available = db.Column(db.Boolean, default=True, nullable=False)
    added_date = db.Column(db.DateTime, nullable=False)
    copies = db.Column(db.String(255), nullable=False)

    def __init__(self, ISBN, author, title, copies):
        """book_information(dict): User book_information

        Usage:
        book <isbn> <author> <title> <copies>
        """
        self.isbn = ISBN
        self.title = title
        self.author = author
        self.available = True
        self.added_date = datetime.now()
        self.copies = copies

    def save(self):
        """Persist the new book in the database
        :param book:
        :return:
        """
        db.session.add(self)
        db.session.commit()
        return {"message": "Success", "BookId": self.isbn}, 200

    def tryupdate(self):
        """Persist the new book in the database
        :param book:
        :return:
        """
        db.session.add(self)
        db.session.commit()
        return {"message": "Success", "BookId": self.isbn}, 200

    def book_delete(self):
        """Persist the new book in the database
        :param book:
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(book_id):
        """
        Filter a user by Id.
        :param user_id:
        :return: User or None
        """
        return Book.query.filter_by(book_id=book_id).first()

    @staticmethod
    def get_many():
        """
        Filter a user by Id.
        :param: blank
        :return: Books or None
        """
        search_vars = {
            'page': request.args.get('page', 1, type=int),
            'isbn': request.args.get('isbn', None, type=str),
            'author': request.args.get('author', default=None, type=str),
            'title': request.args.get('title', None, type=str),
            'copies': request.args.get('copies', "10", type=str),
            'limit': request.args.get('limit', 10, type=int)
        }
        results = Book.search(search_vars)
        itemized = results.items
        return jsonify({
            "page": results.page,
            "total_results": results.total,
            "total_pages": results.pages,
            "per_page": results.per_page,
            "objects": [{'book_id': Book.book_id, 'author': Book.author,
                         'title': Book.title, 'Copies': Book.copies
                         } for Book in itemized
                        ]})

    @staticmethod
    def get_by_isbn(isbn):
        """
        Filter a user by Id.
        :param user_id:
        :return: User or None
        """
        return Book.query.filter_by(isbn=isbn).first()

    def update(self, ISBN, author, title, copies, available):
        """Persist the new book in the database
        :param book:
        :return:
        """
        self.isbn = ISBN
        self.author = author
        self.title = title
        self.copies = copies
        self.available = available
        db.session.add(self)
        db.session.commit()
        return {"message": "Successfuly edited", "BookId": self.isbn}, 200

    def search(filters):
        """
        Method to perform serch on businesses
        using either name location or category
        """
        isbn = filters["isbn"]
        author = filters["author"]
        title = filters["title"]
        copies = filters["copies"]
        page = filters["page"]
        limit = filters['limit']
        query = []
        if isbn:
            query.append(Book.isbn.ilike("%" + isbn + "%"))
        if author:
            query.append(Book.author.ilike("%" + author + "%"))
        if title:
            query.append(Book.title.ilike("%" + title + "%"))
        if copies:
            query.append(Book.copies.ilike("%" + copies + "%"))

        books = Book.query.filter().paginate(page, limit, True)
        #print(books)

        return books


class BorrowedBook(db.Model):
    """Holds details about borrowed books

        Attributes:
            borrow_id: An integer holding a unique book number.
            user_id: A foreign key of type string holding user key.
            book_id: A foreign key of type string holding the book key.
            borrow_date: A date value for when the book was borrowed.
            return_date: A a date value for when the book was returned.
            """
    __tablename__ = 'borrowed_books'
    borrow_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    borrow_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    return_date = db.Column(db.DateTime, nullable=True)
    returned_date = db.Column(db.DateTime, nullable=True)
    return_status = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, book_id):
        """book_information(dict): User book_information

        Usage:
        book <isbn> <author> <title> <copies>
        """
        self.user_id = user_id
        self.book_id = book_id
        self.borrow_date = datetime.now()
        self.return_date = datetime.now() + timedelta(days=7)

    def save(self):
        """Persist the new book in the database
        :param book:
        :return:
        """
        db.session.add(self)
        db.session.commit()
        return {"message": "Borrow Success", "BookId": self.book_id}, 200

    def return_book(self):
        """Persist the new book in the database
        :param book:
        :return:
        """
        self.returned_date = datetime.now()
        self.return_status = True
        db.session.add(self)
        db.session.commit()
        return {"message": "Successfuly returned"}, 200
