import json
import os
import unittest

from app import db
from run import app


class BookTests(unittest.TestCase):
    def setUp(self):
        self.app = app
        app_settings = os.getenv(
            'APP_SETTINGS',
            'app.config.TestingConfig'
        )
        app.config.from_object(app_settings)
        self.BASE_URL = '/api/v1/auth/'
        self.BASE_URL2 = '/api/v1/users/'
        self.BASE_URL3 = '/api/v1/books/'
        self.BASE_URL4 = '/api/v1/books/<int:bookid>/'

        self.client = self.app.test_client()

        db.create_all()

        self.test_user_normal = {
            "username": "Mercy Mbiya",
            "password": "pass123",
            "email": "mbiya@gmail.com"
        }
        self.test_user_admin = {
            'username': 'Dumbledore Prof',
            'password': 'pass123',
            'email': 'prof@gmail.com'
        }
        # input book
        self.test_book = {
            "ISBN": "258",
            "author": "Boniface Mwangi",
            "title": "Unbounded",
            "copies": 19
        }
        self.test_book2 = {
            "ISBN": "259",
            "author": "Chinua Achebe",
            "title": "The old Tree",
            "copies": 11
        }
        self.test_book3 = {
            "ISBN": "260",
            "author": "Maya Angelou",
            "title": "Dancing with the stars",
            "copies": 17
        }

        self.tokens = {}

        self.client.post(
            "/api/v1/auth/register_admin",
            data=json.dumps(self.test_user_admin),
            headers={"content-type": "application/json"})
        self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.test_user_normal),
            headers={"content-type": "application/json"})

        res = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps(self.test_user_admin),
            headers={"content-type": "application/json"})

        self.tokens = res.headers['Authorization']
        self.res_book1 = self.client.post(
            "/api/v1/users/books/",
            data=json.dumps(self.test_book),
            headers={"content-type": "application/json", 'access-token': self.tokens})
        self.client.post(
            "/api/v1/users/books/",
            data=json.dumps(self.test_book2),
            headers={"content-type": "application/json", 'access-token': self.tokens})
        self.client.post(
            "/api/v1/users/books/",
            data=json.dumps(self.test_book3),
            headers={"content-type": "application/json", 'access-token': self.tokens})

        res1 = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'Mercy Mbiya', 'email': 'mbiya@gmail.com', 'password': 'pass123'}),
            headers={"content-type": "application/json"})

        self.tokens2 = res1.headers['Authorization']

    def tearDown(self):
        '''Clean our environment before leaving'''
        self.app.testing = False
        self.app = None
        self.BASE_URL = None
        db.session.remove()
        db.drop_all()

    def test_can_view_all_books(self):
        self.res_book1
        resp = self.client.get(self.BASE_URL3)
        self.assertIn(b'Books retrieved', resp.data)

    def test_can_view_single_book(self):
        one_book = '1'
        self.client.post(
            "/api/v1/auth/register_admin",
            data=json.dumps(self.test_user_admin),
            headers={"content-type": "application/json"})
        res = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps(self.test_user_admin),
            headers={"content-type": "application/json"})
        tokens = res.headers['Authorization']
        res_book = self.client.post(
            "/api/v1/books/",
            data=json.dumps(self.test_book3),
            headers={"content-type": "application/json", 'access-token': self.tokens})
        get_res = self.client.get(self.BASE_URL3+one_book, content_type='application/json', headers={'access-token': tokens})

        self.assertIn('Gets a specific book', str(get_res.data))

    def test_book_not_found(self):
        one_book = '16'
        self.client.post(
            "/api/v1/auth/register_admin",
            data=json.dumps(self.test_user_admin),
            headers={"content-type": "application/json"})
        res = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps(self.test_user_admin),
            headers={"content-type": "application/json"})
        tokens = res.headers['Authorization']
        res_book = self.client.post(
            "/api/v1/books/",
            data=json.dumps(self.test_book3),
            headers={"content-type": "application/json", 'access-token': self.tokens})
        get_res = self.client.get(self.BASE_URL3+one_book, content_type='application/json', headers={'access-token': tokens})

        self.assertIn('Item not found', str(get_res.data))

    def test_can_delete_book(self):
        one_book = '1'
        self.client.post(
            "/api/v1/auth/register_admin",
            data=json.dumps(self.test_user_admin),
            headers={"content-type": "application/json"})
        res = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps(self.test_user_admin),
            headers={"content-type": "application/json"})
        tokens = res.headers['Authorization']
        res_book = self.client.post(
            "/api/v1/books/",
            data=json.dumps(self.test_book3),
            headers={"content-type": "application/json", 'access-token': self.tokens})
        get_res = self.client.delete(self.BASE_URL3+one_book, content_type='application/json', headers={'access-token': tokens})

        self.assertIn('Success, Book deleted', str(get_res.data))


if __name__ == '__main__':
    unittest.main()
