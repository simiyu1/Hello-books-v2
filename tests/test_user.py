class UserTests(unittest.TestCase):
    def setUp(self):
        # Prepare for testing;set up variables
        from app.user.views import users_list
        self.all_users = users_list
        self.app = app
        self.app = self.app.test_client()
        self.BASE_URL = 'http://localhost:5000/api/v1/auth/'
        self.BASE_URL2 = 'http://localhost:5000/api/v1/users/'

    def tearDown(self):
        '''Clean our environment before leaving'''
        self.app.testing = False
        self.app = None
        self.BASE_URL = None
        self.all_users = None
        self.user = None

    def test_can_create_user(self):
        self.user = {'userid': 3, 'username': 'Juma', 'password': 'pass123'}
        resp = self.app.post(self.BASE_URL + 'register', data=json.dumps(
            self.user), content_type='application/json')
        self.assertEqual(resp.status_code, 201,
                         msg="user created")

    def test_can_create_user_fail_username_exists(self):
        self.user = {"userid": 3, 'username': 'Juma', 'password': 'pass123'}
        resp = self.app.post(self.BASE_URL + 'register', data=json.dumps(
            self.user), content_type='application/json')
        self.assertEqual(resp.status_code, 409,
                         msg="username exists please try another")

    def test_can_login_user_pass(self):
        self.successuser = {'username': 'Kinde Kinde', 'password': 'pass123'}
        responce = self.app.post(self.BASE_URL + 'login', data=json.dumps(
            self.successuser), content_type='application/json')
        self.assertEqual(responce.status_code, 202,
                         msg="Welcome, login success")

    def test_can_login_user_fails(self):
        self.successuser = {'username': 'Miguna', 'password': 'kenyan'}
        resp = self.app.post(self.BASE_URL + 'login', data=json.dumps(
            self.successuser), content_type='application/json')
        self.assertEqual(resp.status_code, 401,
                         msg="Check username or password and try again")

    def test_can_logout_user(self):
        self.successuser = {'username': 'Miguna'}
        resp = self.app.post(self.BASE_URL + 'logout', data=json.dumps(
            self.successuser), content_type='application/json')
        self.assertEqual(resp.status_code, 200,
                         msg="Successful you are logged out")

    def test_can_logout_user_fail(self):
        self.successuser = {'username': 'Migunaa'}
        resp = self.app.post(self.BASE_URL + 'logout', data=json.dumps(
            self.successuser), content_type='application/json')
        self.assertEqual(resp.status_code, 401,
                         msg="user unknown")

    def test_can_get_user_fail(self):
        self.userid = '?userid=117'
        responce = self.app.get(self.BASE_URL2 + self.userid)
        self.assertEqual(responce.status_code, 404,
                         msg="User not found")

    def test_can_get_users_list_fail(self):
        self.userid = '?userid=3'
        responce = self.app.get(self.BASE_URL2 + self.userid)
        self.assertEqual(responce.status_code, 404,
                         msg="User not found")

    def test_can_get_user(self):
        self.userid = '?userid=2'
        responce = self.app.get(self.BASE_URL2 + self.userid)
        self.assertEqual(responce.status_code, 200,
                         msg="Fetched user")

    def test_can_get_all_users(self):
        responce = self.app.get(self.BASE_URL2)
        self.assertEqual(responce.status_code, 200,
                         msg="Fetched User")

    def test_can_reset_password(self):
        self.resetdata = {'username': 'Kinde Kinde', 'password': 'pass123', 'new_password': 'canadian'}
        resp = self.app.post(self.BASE_URL + 'reset', data=json.dumps(
            self.resetdata), content_type='application/json')
        self.assertEqual(resp.status_code, 202,
                         msg="Reset success")

    def test_can_reset_password_fail(self):
        self.resetdata = {'username': 'Miguna', 'password': 'canadian', 'new_password': 'kenyan'}
        resp = self.app.post(self.BASE_URL + 'reset', data=json.dumps(
            self.resetdata), content_type='application/json')
        self.assertEqual(resp.status_code, 201,
                         msg="No user or password found")

    def test_can_reset_fields_empty(self):
        self.resetdata = {'username': 'Miguna'}
        resp = self.app.post(self.BASE_URL + 'reset', data=json.dumps(
            self.resetdata), content_type='application/json')
        self.assertEqual(resp.status_code, 500,
                         msg="Make sure to fill all required fields")

    def test_user_can_borrow_a_book(self):
        data = {"userid": 4}
        self.book_data = "4"
        # send the data
        resp = self.app.post('http://localhost:5000/api/v1/users/books/' + self.book_data,
                             data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200, msg='Book borrowed')

    def test_user_can_borrow_a_book_no_user_details(self):
        self.book_data = "4"
        # send the data
        resp = self.app.post('http://localhost:5000/api/v1/users/books/' + self.book_data)
        self.assertEqual(resp.status_code, 401, msg='User details missing')

    def test_user_can_borrow_a_book_not_logged_in(self):
        data = {"userid": 2}
        self.book_data = "4"
        # send the data
        resp = self.app.post('http://localhost:5000/api/v1/users/books/' + self.book_data,
                             data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 406, msg='Not logged in')

    def test_book_not_exist(self):
        data = {"userid": 4}
        self.book_data = "18"
        # send the data
        resp = self.app.post('http://localhost:5000/api/v1/users/books/' + self.book_data,
                             data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 404, msg='no book found with the given id')


if __name__ == '__main__':
    unittest.main()
