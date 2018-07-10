from tests.helper_tests import InitTests

import json
import unittest


class UserTests(unittest.TestCase):
    def setUp(self):
        InitTests.testSetUp(self)

    

    def test_can_create_user(self):
        self.user = {"email": "juma@ymail.com", "username": "Juma", "password": "pass123"}
        resp = self.client.post(self.BASE_URL + 'register', data=json.dumps(
            self.user), content_type='application/json')
        self.assertEqual(resp.status_code, 201,
                         msg="Successfully registered")

    def test_can_fetch_user(self):
        resp = self.client.get(self.BASE_URL2 + '1', content_type='application/json', headers={'access-token': self.tokenadmin})
        self.assertIn('Gets a specific user', str(resp.data))

    def test_can_get_all_users(self):
        responce = self.client.get(self.BASE_URL2, headers={'access-token': self.tokenadmin})
        self.assertEqual(responce.status_code, 200,
                         msg="Fetched User")

    def test_can_get_user_fail(self):
        self.userid = '?userid=117'
        responce = self.client.get(self.BASE_URL + self.userid)
        self.assertEqual(responce.status_code, 404,
                         msg="User not found")

    def test_can_get_users_list_fail(self):
        self.userid = '13'
        responce = self.client.get(self.BASE_URL2 + self.userid, headers={'access-token': self.tokenadmin})
        self.assertEqual(responce.status_code, 404,
                         msg="User not found")

    def test_can_borrow_book(self):
        self.res_book
        bookid = '1'
        responce = self.client.post(self.BASE_URL3 + bookid, headers={'access-token': self.tokenadmin})
        self.assertIn('Borrow Success', str(responce.data))

    def test_can_borrow_book_fail(self):
        bookid = '10'
        responce = self.client.post(self.BASE_URL3 + bookid, headers={'access-token': self.tokenadmin})
        self.assertIn('Book not found', str(responce.data))

    def test_can_borrow_book_fail_token(self):
        bookid = '10'
        responce = self.client.post(self.BASE_URL3 + bookid)
        self.assertIn('Token is missing, login to get token', str(responce.data))

    def test_can_return_book(self):
        self.res_book
        self.res_book2
        self.borrow_book
        bookid = '1'
        responce = self.client.put(self.BASE_URL3 + bookid, headers={'access-token': self.tokenadmin})
        self.assertIn('Return Success', str(responce.data))

    def test_can_return_book_fail(self):
        bookid = '12'
        response = self.client.put(self.BASE_URL3 + bookid, headers={'access-token': self.tokenadmin})
        print(self.tokenadmin)
        self.assertIn('book not found', str(response.data))

    

if __name__ == '__main__':
    unittest.main()
