from app import db
from datetime import datetime


class Book(db.Model):
    """A book in the library or borrowed

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
    def get_many_by_id(book_id):
        """
        Filter a user by Id.
        :param user_id:
        :return: User or None
        """
        return Book.query.filter_by(book_id=book_id).first()

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
        self.isbn= ISBN
        self.author= author
        self.title= title
        self.copies= copies
        self.available= available
        db.session.add(self)
        db.session.commit()
        return {"message": "Successfuly edited", "BookId": self.isbn}, 200
