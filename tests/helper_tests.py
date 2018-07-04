import json
import os
import unittest

from app import db
from run import app


class InitTests:
    def testSetUp(self):
        self.app = app
        app_settings = os.getenv(
            'APP_SETTINGS',
            'app.config.TestingConfig'
        )
        app.config.from_object(app_settings)
        self.BASE_URL = '/api/v1/auth/'
        self.BASE_URL2 = '/api/v1/users/'
        self.BASE_URL3 = '/api/v1/users/books/'
        self.BASE_URL4 = '/api/v1/books/<int:bookid>/'
        self.BASE_URL5 = '/api/v1/books/'

        self.client = self.app.test_client()

        db.create_all()

        self.test_user_normal = {
            "username": "Mercy Mbiya",
            "password": "pass123",
            "email": "mbiya@gmail.com"
        }
        self.test_user_admin = {
            "username": "Dumbledore Prof",
            "password": "pass123",
            "email": "prof@gmail.com"
        }
        #input book
        self.test_book = {
            "ISBN": "258",
            "author": "Boniface Mwangi",
            "title": "Unbounded",
            "copies": 19
        }
        self.test_book_update = {
            "ISBN": "261",
            "author": "Ngugi Wa Thiongó",
            "title": "The river and the source",
            "copies": 4
        }
        self.test_book2 = {
            "ISBN": "259",
            "author": "Chinua Achebe",
            "title": "A time to heal",
            "copies": 1
        }
        self.test_book3 = {
            "ISBN": "260",
            "author": "Maya Angelou",
            "title": "Dancing with the stars",
            "copies": 17
        }
        #incomplete book details
        self.test_book_empty = {
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
            data=json.dumps({'username': 'Dumbledore Prof', 'email': 'prof@gmail.com', 'password': 'pass123'}),
            headers={"content-type": "application/json"})
        res1 = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'Mercy Mbiya', 'email': 'mbiya@gmail.com', 'password': 'pass123'}),
            headers={"content-type": "application/json"})

        self.tokens = res.headers['Authorization']
        self.res_book = self.client.post(
            "/api/v1/books/",
            data=json.dumps(self.test_book),
            headers={"content-type": "application/json", 'access-token': self.tokens})
        self.res_book2 = self.client.post(
            "/api/v1/books/",
            data=json.dumps(self.test_book2),
            headers={"content-type": "application/json", 'access-token': self.tokens})
        self.borrow_book = self.client.post(
            "/api/v1/users/books/1",
            headers={"content-type": "application/json", 'access-token': self.tokens})

        self.res1 = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'Mercy Mbiya', 'email': 'mbiya@gmail.com', 'password': 'pass123'}),
            headers={"content-type": "application/json"})

        self.tokens2 = res1.headers['Authorization']


    def testTearDown(self):
        '''Clean our environment before leaving'''
        self.app.testing = False
        self.app = None
        self.BASE_URL = None
        db.session.remove()
        db.drop_all()