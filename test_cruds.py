import unittest
import json

from run import app
from app.bookdir.models import *
from app.bookdir.views import books_list


class BookAPITests(unittest.TestCase):

    def setUp(self):
        """Define test (env) variables and initialize some list data for the app."""
        self.app = app
        # creating dummy instances.
        # books_list = []
        # book1 = Book(1,'The Eleventh Commandment','Jeffrey Archer')
        # book2 = Book(2,'If Tomorrow Comes','Sidney Sheldon')
        # book3 = Book(3,'Origin','Dan Brown')
        # books_list.append(book1)
        # books_list.append(book2)
        # books_list.append(book3)

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
        data= {'ISBN': 3}
        resp = self.app.get(self.BASE_URL,
                             data=json.dumps(data), content_type='application/json')
        data = json.loads(resp.get_data().decode('utf-8'))
        # Later check that test_item should be in the list book7 in data
        self.assertTrue(data, msg='All book data')

    def test_get_book_fail(self):
        ''' Should fail book retrieval for unkown ISBN
        '''
        data= {'ISBN': 33}
        resp = self.app.get(self.BASE_URL,
                             data=json.dumps(data), content_type='application/json')
        # Later check that test_item should be in the list book7 in data
        self.assertEqual(resp.status_code, 200 , msg='Books not found')

    def test_get_a_single_book_by_isbn(self):
        ''' test if a book cab be searched by ISBN
        '''
        sent_data= "?ISBN=2"
        resp = self.app.get(self.BASE_URL+sent_data)

        data = json.loads(resp.get_data().decode('utf-8'))
        got_data = data[0]

        test_item = {'ISBN': 1, 'title':'The Eleventh Commandment','author':'Jeffrey Archer'}


        # test_item should be in the list
        self.assertEqual(test_item['title'], got_data['title'],
                        msg='Gets a specific book')

    def test_post_book(self):
        '''This method tests that a book can be added'''
        newbook = {'ISBN': 10, 'title':'The hand of God',
                      'author':'Ken Follet'}
        resp = self.app.post(self.BASE_URL, data=json.dumps(
            newbook), content_type='application/json')
        self.assertEqual(resp.status_code, 201,
                         msg='Book added')

    def test_delete_book(self):
        ''' testing book deletion
        '''
        ISBN = "2"
        resp = self.app.delete(self.BASE_URL+ISBN)
        test_item = (2,'If Tomorrow Comes','Sidney Sheldon')
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
        responce = self.app.delete(self.BASE_URL+ISBN)
        self.assertEqual(responce.status_code, 404,
                         msg='Book entry not found')

    def test_edit_book_fail(self):
        ''' testing book put
        '''
        data= {'ISBN': 26}
        resp = self.app.put(self.BASE_URL, data=json.dumps(
            data), content_type='application/json')
        self.assertEqual(resp.status_code, 406,
                         msg='Missing book details')

    def test_update_book_success(self):
        '''This method updates book details given an ISBN number'''
        new_book = {'title':'The hand of God',
                      'author':'Ken Follet'}
        ISBN = "3"
        resp = self.app.put(self.BASE_URL+ISBN, data=json.dumps(
            new_book), content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_update_book(self):
        '''This method updates book details given an ISBN number'''
        new_book = {'ISBN': 10, 'title':'The hand of God',
                      'author':'Ken Follet'}
        resp = self.app.put(self.BASE_URL, data=json.dumps(
            new_book), content_type='application/json')
        self.assertEqual(resp.status_code, 406,
                         msg='Book added')
    
    def test_update_book_missing_details(self):
        '''This method throws error message when variables are missing'''
        new_book = { 'title':'The hand of God',
                      'author':'Ken Follet'}
        resp = self.app.put(self.BASE_URL, data=json.dumps(
            new_book), content_type='application/json')
        self.assertEqual(resp.status_code, 406,
                         msg='Missing book details')

    def test_update_book_not_exist(self):
        '''This method throws error message when the book is unavailable'''
        new_book = { 'title':'The hand of God',
                      'author':'Ken Follet'}
        ISBN = "23"
        resp = self.app.put(self.BASE_URL+ISBN, data=json.dumps(
            new_book), content_type='application/json')
        self.assertEqual(resp.status_code, 401,
                         msg='Book to udate not found')

class UserTests(unittest.TestCase):
    def setUp(self):
        # Prepare for testing;set up variables
        from app.userdir.views import users_list
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
        self.user = {'userid':3,'username': 'Juma', 'password': 'pass123'}
        resp = self.app.post(self.BASE_URL + 'register', data=json.dumps(
            self.user), content_type='application/json')
        self.assertEqual(resp.status_code, 201,
                        msg="user created")
  
    def test_can_create_user_fail_username_exists(self):
        self.user = {"userid":3 ,'username': 'Juma', 'password': 'pass123'}
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
        resp = self.app.post('http://localhost:5000/api/v1/users/books/'+self.book_data,
                             data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200, msg='Book borrowed')

    def test_user_can_borrow_a_book_no_user_details(self):
        self.book_data = "4"
        # send the data
        resp = self.app.post('http://localhost:5000/api/v1/users/books/'+self.book_data)
        self.assertEqual(resp.status_code, 401, msg='User details missing')

    def test_user_can_borrow_a_book_not_logged_in(self):
        data = {"userid": 2}
        self.book_data = "4"
        # send the data
        resp = self.app.post('http://localhost:5000/api/v1/users/books/'+self.book_data,
                              data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 406, msg='Not logged in')

    def test_book_not_exist(self):
        data = {"userid": 4}
        self.book_data = "18"
        # send the data
        resp = self.app.post('http://localhost:5000/api/v1/users/books/'+self.book_data,
                              data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 404, msg='no book found with the given id')

if __name__ == '__main__':
    unittest.main()
