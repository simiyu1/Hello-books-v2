import json
import os
import unittest
from tests.helper_tests import InitTests

from app import db
from run import app


class BookTests(unittest.TestCase):
    def setUp(self):
        InitTests.testSetUp(self)

    def tearDown(self):
        InitTests.testTearDown(self)

    def test_can_view_all_books(self):
        self.res_book
        resp = self.client.get(self.BASE_URL5)
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
        get_res = self.client.get(self.BASE_URL5 + one_book, content_type='application/json',
                                  headers={'access-token': tokens})

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
        get_res = self.client.get(self.BASE_URL5 + '16')

        self.assertIn('Item not found', str(get_res.data))

    def test_can_delete_book(self):
        one_book = '2'
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
        res_book = self.client.post(
            "/api/v1/books/",
            data=json.dumps(self.test_book2),
            headers={"content-type": "application/json", 'access-token': self.tokens})
        get_res = self.client.delete(self.BASE_URL5 + one_book, content_type='application/json',
                                     headers={'access-token': tokens})

        self.assertIn('Success, Book deleted', str(get_res.data))

    def test_can_delete_book_fail_no_id(self):
        one_book = '11'
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
        get_res = self.client.delete(self.BASE_URL5 + one_book, content_type='application/json',
                                     headers={'access-token': tokens})

        self.assertIn('book entry not found', str(get_res.data))

    def test_can_edit_book(self):
        book_id = '1'
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
        get_res = self.client.put(self.BASE_URL5 + book_id, content_type='application/json',
                                  data=json.dumps(self.test_book_update),
                                  headers={'access-token': tokens})
        self.assertIn('Success, Book updated', str(get_res.data))

    def test_can_edit_book_bad_id(self):
        book_id = '11'
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
        get_res = self.client.put(self.BASE_URL5 + book_id, content_type='application/json',
                                  data=json.dumps(self.test_book2),
                                  headers={'access-token': tokens})
        self.assertIn('message": "book to update not found', str(get_res.data))

    def test_can_edit_book_no_details(self):
        book_id = '1'
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
        get_res = self.client.put(self.BASE_URL5 + book_id, content_type='application/json',
                                  data=json.dumps(self.test_book_empty),
                                  headers={'access-token': tokens})
        self.assertIn('message": "book details missing', str(get_res.data))


if __name__ == '__main__':
    unittest.main()
