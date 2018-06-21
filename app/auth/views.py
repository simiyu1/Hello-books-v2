
from flask_restful import Resource
from flask import request, jsonify
from app import bcrypt

from app.userdir.models import User, BlackListToken
from app.auth.helper import response, response_auth
import re
#from app.userdir.views import users_list


# small_users_list = []
# user5 = User(5,'Miguna','pass123')
# user6 = User(6,'Mboys','pass123')
# user6.active = True
# small_users_list.append(user5)
# small_users_list.append(user6)


class Register(Resource):
    '''User registration Class'''

    @classmethod
    def post(self):
        req_data = request.get_json()
        if not req_data['username'] or not req_data['password']:
            return {"message": "username or password missing"}, 400
        username = req_data['username']
        email = req_data['email']
        password = req_data['password']
        # exists = [
        #     user for user in users_list if user.username == username]
        #
        # if exists:
        #     return {"message": "username exists please try another"},409
        '''if request.content_type == 'application/json':
            post_data = request.get_json()
            email = post_data.get('email')
            password = post_data.get('password')
            if re.match(r"[^@]+@[^@]+\.[^@]+", email) and len(password) > 4:
                user = User.get_by_email(email)
        user_exists = User.get_by_email(email)'''
        username_exists = User.get_by_username(username)
        email_exists = User.get_by_email(email)
        if not username_exists or not email_exists:
            token = User(email=email, password=password, username=username).save()
            # return response_auth('success', 'Successfully registered', token, 201)
            #return jsonify({"Token": token})
            return {"message": "Successfully registered","Token": token}, 200
        else:
            return {"message": "Failed, Username or email already exists, Please sign In"}, 400


class Login(Resource):
    '''User login Class'''

    @classmethod
    def post(self):
        req_data = request.get_json()
        if not req_data['email'] or not req_data['password']:
            return {"message": "username or password missing"}, 406
        username = req_data['username']
        password = req_data['password']
        email = req_data['email']
        if re.match(r"[^@]+@[^@]+\.[^@]+", email) and len(password) > 4:
            user = User.query.filter_by(username=username).first()
            chkemail = User.query.filter_by(email=email).first()
            if user or chkemail and bcrypt.check_password_hash(user.password, password):
                return response_auth('success', 'Successfully logged In', user.encode_auth_token(user.id), 200)
            return response('failed', 'User does not exist or password is incorrect', 401)
        return {"message":"Check your password or username and try again"}, 401


class Reset(Resource):

    @classmethod
    def post(self):
        req_data = request.get_json()
        if not req_data['username'] or not req_data['password'] or not req_data['new_password'] or not req_data['confirm_new_password']:
            return {"message": "make sure to fill all required fields"}, 400
        username = req_data['username']
        password = req_data['password']
        new_password = req_data['new_password']
        confirm_new_password = req_data['confirm_new_password']
        user = User.query.filter_by(username=username).first()
        if not password or not new_password or not confirm_new_password:
            return response('message', "No user or password found", 400)
        if bcrypt.check_password_hash(user.password, password.encode('utf-8')):
            if not new_password == new_password:
                return response('failed', 'New Passwords do not match', 400)
            if not len(new_password) > 4:
                return response('failed', 'New password should be greater than four characters long', 400)
            user.reset_password(new_password)
            return response('success', 'Password reset successfully', 200)
        return response('failed', "Incorrect password", 401)
        return response('failed', 'Content type must be json', 400)


class Logout(Resource):

    @classmethod
    def post(self):
        """
        Try to logout a user using a token
        :return: JSon Response
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                return response('failed', 'Provide a valid auth token', 403)
            else:
                decoded_token_response = User.decode_auth_token(auth_token)
                if not isinstance(decoded_token_response, str):
                    token = BlackListToken(auth_token)
                    token.blacklist()
                    return response('success', 'Successfully logged out', 200)
                return response('failed', decoded_token_response, 401)
        return response('failed', 'Provide an authorization header', 403)
