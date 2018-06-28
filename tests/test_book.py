import unittest
import json

from run import app
from app.book.models import *
from app.book.views import *


class BookAPITests(unittest.TestCase):

    def setUp(self):
        """Define test (env) variables and initialize some list data for the app."""
        self.app = app
        self.app = self.app.test_client()
        self.BASE_URL = 'http://127.0.0.1:5000/api/v1/books/'

    def tearDown(self):
        '''Clean our environment before leaving'''
        self.app.testing = False
        self.app = None
        self.BASE_URL = None

    def test_get_all_books(self):
        ''' Should retrieve books from library
        '''
        resp = self.app.get(self.BASE_URL)
        data = json.loads(resp.get_data().decode('utf-8'))
        # Later check that test_item should be in the list book7 in data
        self.assertTrue(data, msg='All book data')

    def test_get_books_by_ISBN(self):
        ''' Should retrieve books from library by ISBN
        '''
        data = {'ISBN': 3}
        resp = self.app.get(self.BASE_URL,
                            data=json.dumps(data), content_type='application/json')
        data = json.loads(resp.get_data().decode('utf-8'))
        # Later check that test_item should be in the list book7 in data
        self.assertTrue(data, msg='All book data')

    def test_get_book_fail(self):
        ''' Should fail book retrieval for unkown ISBN
        '''
        data = {'ISBN': 33}
        resp = self.app.get(self.BASE_URL,
                            data=json.dumps(data), content_type='application/json')
        # Later check that test_item should be in the list book7 in data
        self.assertEqual(resp.status_code, 200, msg='Books not found')

    def test_get_a_single_book_by_isbn(self):
        ''' test if a book cab be searched by ISBN
        '''
        sent_data = "?ISBN=2"
        resp = self.app.get(self.BASE_URL + sent_data)

        data = json.loads(resp.get_data().decode('utf-8'))
        got_data = data[0]

        test_item = {'ISBN': 1, 'title': 'The Eleventh Commandment', 'author': 'Jeffrey Archer'}

        # test_item should be in the list
        self.assertEqual(test_item['title'], got_data['title'],
                         msg='Gets a specific book')

    def test_post_book(self):
        '''This method tests that a book can be added'''
        newbook = {'ISBN': 10, 'title': 'The hand of God',
                   'author': 'Ken Follet'}
        resp = self.app.post(self.BASE_URL, data=json.dumps(
            newbook), content_type='application/json')
        self.assertEqual(resp.status_code, 201,
                         msg='Book added')

    def test_delete_book(self):
        ''' testing book deletion
        '''
        ISBN = "2"
        resp = self.app.delete(self.BASE_URL + ISBN)
        test_item = (2, 'If Tomorrow Comes', 'Sidney Sheldon')
        # Get all books in the api
        books = []
        for book in books_list:
            books.append(book.ISBN)
        self.assertFalse(test_item in books,
                         msg='The api should delete a book')

    def test_delete_book_not_found(self):
        ''' testing book deletion when not available
        '''
        ISBN = "26"
        responce = self.app.delete(self.BASE_URL + ISBN)
        self.assertEqual(responce.status_code, 404,
                         msg='Book entry not found')

    def test_edit_book_fail(self):
        ''' testing book put
        '''
        data = {'ISBN': 26}
        resp = self.app.put(self.BASE_URL, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(resp.status_code, 406,
                         msg='Missing book details')

    def test_update_book_success(self):
        '''This method updates book details given an ISBN number'''
        new_book = {'title': 'The hand of God',
                    'author': 'Ken Follet'}
        ISBN = "3"
        resp = self.app.put(self.BASE_URL + ISBN, data=json.dumps(
            new_book), content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_update_book(self):
        '''This method updates book details given an ISBN number'''
        new_book = {'ISBN': 10, 'title': 'The hand of God',
                    'author': 'Ken Follet'}
        resp = self.app.put(self.BASE_URL, data=json.dumps(
            new_book), content_type='application/json')
        self.assertEqual(resp.status_code, 406,
                         msg='Book added')

    def test_update_book_missing_details(self):
        '''This method throws error message when variables are missing'''
        new_book = {'title': 'The hand of God',
                    'author': 'Ken Follet'}
        resp = self.app.put(self.BASE_URL, data=json.dumps(
            new_book), content_type='application/json')
        self.assertEqual(resp.status_code, 406,
                         msg='Missing book details')

    def test_update_book_not_exist(self):
        '''This method throws error message when the book is unavailable'''
        new_book = {'title': 'The hand of God',
                    'author': 'Ken Follet'}
        ISBN = "23"
        resp = self.app.put(self.BASE_URL + ISBN, data=json.dumps(
            new_book), content_type='application/json')
        self.assertEqual(resp.status_code, 401,
                         msg='Book to udate not found')
