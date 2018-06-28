import unittest
import json, os

from app import db
from run import app


class UserTests(unittest.TestCase):
    def setUp(self):
        self.app = app
        app_settings = os.getenv(
            'APP_SETTINGS',
            'app.config.TestingConfig'
        )
        app.config.from_object(app_settings)
        self.BASE_URL = '/api/v1/auth/'
        self.BASE_URL2 = '/api/v1/users/'

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

        self.tokens = res.headers['Authorization']
        self.client.post(
            "/api/v1/users/books/",
            data=json.dumps(self.test_book),
            headers={"content-type": "application/json",'access-token': self.tokens})

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

    def test_can_create_user(self):
        self.user = {"email": "juma@ymail.com", "username": "Juma", "password": "pass123"}
        resp = self.client.post(self.BASE_URL + 'register', data=json.dumps(
            self.user), content_type='application/json')
        self.assertEqual(resp.status_code, 201,
                         msg="Successfully registered")

    def test_can_create_user_fail_username_exists(self):
        self.user = {"email": "mbiy@gmail", "username": "Mercy Mbiya", 'password': 'pass123'}
        resp = self.client.post(self.BASE_URL + 'register', data=json.dumps(
            self.user), content_type='application/json')
        self.assertEqual(resp.status_code, 409,
                         msg="Failed, Username or email already exists, Please sign In")

    def test_can_login_user_pass(self):
        self.successuser = {"username": "Mercy Mbiya", "password": "pass123", "email": "mbiya@gmail.com"}
        responce = self.client.post(self.BASE_URL + 'login', data=json.dumps(
            self.successuser), content_type='application/json')
        self.assertEqual(responce.status_code, 200,
                         msg="Successfully logged In")

    def test_can_login_user_fails(self):
        self.successuser = {"username": "Mercy Mbiya", "password": "Badpass123", "email": "mbiya@gmail.com"}
        respo = self.client.post(self.BASE_URL + 'login', data=json.dumps(
            self.successuser), content_type='application/json')
        self.assertTrue(respo.status_code, 401)

    def test_can_logout_user(self):
        resp = self.client.post(self.BASE_URL + 'logout', content_type='application/json', headers={'access-token': self.tokens})
        self.assertEqual(resp.status_code, 200,
                         msg="Successful you are logged out")

    def test_can_logout_user_fail(self):
        resp = self.client.post(self.BASE_URL + 'logout', content_type='application/json')
        self.assertEqual(resp.status_code, 200,
                         msg="user unknown")

    def test_can_get_user_fail(self):
        self.userid = '?userid=117'
        responce = self.client.get(self.BASE_URL + self.userid)
        self.assertEqual(responce.status_code, 404,
                         msg="User not found")

    def test_can_get_users_list_fail(self):
        self.userid = '13'
        responce = self.client.get(self.BASE_URL2 + self.userid, headers={'access-token': self.tokens})
        self.assertEqual(responce.status_code, 404,
                         msg="User not found")

    def test_can_get_user(self):
        self.userid = '1'
        response = self.client.get(self.BASE_URL2 + self.userid, headers={'access-token': self.tokens})
        self.assertEqual(response.status_code, 200,
                         msg="Gets a specific user")

    def test_can_get_all_users(self):
        responce = self.client.get(self.BASE_URL2, headers={'access-token': self.tokens})
        self.assertEqual(responce.status_code, 200,
                         msg="Fetched User")

    def test_can_reset_password(self):
        self.resetdata = {"username": "Mercy Mbiya", 'password': 'pass123', 'new_password': 'pass456',
                          'confirm_new_password': 'pass456'}
        resp = self.client.post(self.BASE_URL + 'reset', data=json.dumps(
            self.resetdata), content_type='application/json')
        self.assertEqual(resp.status_code, 200,
                         msg="Reset success")

    def test_can_reset_password_fail(self):
        self.resetdata = {"username": "Mercy Mbiya", 'password': 'pass123', 'new_password': 'canadian123',
                          'confirm_new_password': 'can123'}
        resp = self.client.post(self.BASE_URL + 'reset', data=json.dumps(
            self.resetdata), content_type='application/json', headers={'access-token': self.tokens})
        self.assertEqual(resp.status_code, 200,
                         msg="New Passwords do not match")

    def test_can_reset_fields_empty(self):
        self.resetdata = {'username': 'Miguna'}
        resp = self.client.post(self.BASE_URL + 'reset', data=json.dumps(
            self.resetdata), content_type='application/json', headers={'access-token': self.tokens})
        self.assertEqual(resp.status_code, 400,
                         msg="Make sure to fill all required fields")

    def test_book_not_found(self):
        self.book_data = "1"
        resp = self.client.post('/api/v1/users/books/' + self.book_data,
                                content_type='application/json',
                                headers={'access-token': self.tokens})
        self.assertEqual(resp.status_code, 404, msg='Book not found')


    def test_user_can_borrow_a_book_not_logged_in(self):
        data = {"userid": 2}
        self.book_data = "4"
        # send the data
        resp = self.client.post('/api/v1/users/books/' + self.book_data,
                                content_type='application/json', headers={'Authorization': 'Bearer '})
        self.assertEqual(resp.status_code, 401, msg='Token is missing, login to get token')

    def test_book_not_exist(self):
        self.book_data = "18"
        # send the data
        resp = self.client.post('/api/v1/users/books/' + self.book_data,
                                content_type='application/json', headers={'access-token': self.tokens})
        self.assertEqual(resp.status_code, 404, msg='Item not found')


if __name__ == '__main__':
    unittest.main()
