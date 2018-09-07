
from flask_restful import Resource
from flask import request, jsonify
from app import bcrypt

from app.user.models import User, BlackListToken
from app.auth.helper import response, response_auth, login_response_auth
import re


class Register(Resource):
    '''User registration Class

    :param email:
    :param username:
    :param password:
    :return: JSON
    '''

    @classmethod
    def post(self):
        req_data = request.get_json()
        if not req_data['username'] or not req_data['password']:
            return {"message": "username or password missing"}, 400
        username = req_data['username']
        email = req_data['email']
        password = req_data['password']
        username_exists = User.get_by_username(username)
        email_exists = User.get_by_email(email)
        if not username_exists and not email_exists:
            User(email=email, password=password, username=username).save()
            return {"message": "Successfully registered"}, 201
        else:
            return {"message": "Failed, Username or email already exists, Please sign In"}, 409

class RegisterAdmin(Resource):
    '''Register an Admin user

    :param email:
    :param username:
    :param password:
    :return: JSON
    '''

    @classmethod
    def post(self):
        req_data = request.get_json()
        if not req_data['username'] or not req_data['password']:
            return {"message": "username or password missing"}, 400
        username = req_data['username']
        email = req_data['email']
        password = req_data['password']
        username_exists = User.get_by_username(username)
        email_exists = User.get_by_email(email)
        if not username_exists and not email_exists:
            User(email=email, password=password, username=username).make_admin()
            return {"message": "Successfully registered"}, 200
        else:
            return {"message": "Failed, Username or email already exists, Please sign In"}, 400


class Login(Resource):
    '''User login Class

    :param email:
    :param username: or
    :param password:
    :return: JSON
    '''

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
            
            # this_user_id = User.decode_auth_token(token)
            # current_user = User.get_by_id(this_user_id)
            # current_role = current_user.role


            if (user or chkemail) and bcrypt.check_password_hash(user.password, password):
                current_role = user.role
                return login_response_auth('success', 'Successfully logged In', user.encode_auth_token(user.id), 500, username, current_role )
            return {'message': 'User does not exist or password is incorrect'}, 401
        return {"message": "Check your password or username and try again"}, 401


class Reset(Resource):
    '''User Reset Password Class

        :param username:
        :param password:
        :param new_password:
        :return: JSON
        '''

    @classmethod
    def post(self):
        req_data = request.get_json()
        if not 'new_password' in req_data or not 'confirm_new_password' in req_data:
            return {'message': "Make sure to fill all required fields"}, 400
        else:
            password = req_data['password']
            new_password = req_data['new_password']
            confirm_new_password = req_data['confirm_new_password']
            auth_header = request.headers['access_token']

            auth_token = request.headers['access-token']
            this_user_id = User.decode_auth_token(auth_token)
            if auth_header:
                try:
                    #auth_token = auth_header.split(" ")[1]
                    auth_token = request.headers['access-token']
                    user_id = User.decode_auth_token(auth_token)
                except IndexError:
                    return response('failed', 'Provide a valid auth token', 403)
                else:
                    decoded_token_response = User.decode_auth_token(auth_token)
                    if not isinstance(decoded_token_response, str):
                        this_user = User.get_by_id(user_id)
                        user = User.query.filter_by(username="Boss Baby").first()
                        print(">>>>>>>>>>>>>>>>>>>>>",user)
                        print(bcrypt.check_password_hash(user.password, password.encode('utf-8')))
                        if bcrypt.check_password_hash(this_user.password, password.encode('utf-8')):
                            if new_password != confirm_new_password:
                                return response('failed', 'New Passwords do not match', 400)
                            if not len(new_password) > 4:
                                return response('failed', 'New password should be greater than four characters long',
                                                400)
                            this_user.reset_password(new_password)
                            return response('success', 'Password reset successfully', 2001)
                        return response('success', 'Successfully logged out', 2002)
                    return response('failed', decoded_token_response, 401)
            return response('failed', 'Provide an authorization header', 403)


class Logout(Resource):

    @classmethod
    def post(self):
        """
        Try to logout a user using a token
        :return: JSon Response
        """
        #auth_header = request.headers.get('Authorization')
        token = None
        if 'access-token' not in request.headers:
            return response('failed', 'Provide an authorization header', 403)
        try:
            auth_token = request.headers['access-token']
            this_user_id = User.decode_auth_token(auth_token)
            current_user = User.get_by_id(this_user_id)
        except IndexError:
                return response('failed', 'Provide a valid auth token', 403)
        else:
                decoded_token_response = User.decode_auth_token(auth_token)
                if not isinstance(decoded_token_response, str):
                    this_user = User.get_by_id(this_user_id)
                    this_user.set_loggedin_false()
                    token = BlackListToken(auth_token)
                    token.blacklist()
                    return response('success', 'Successfully logged out', 200)
                return response('failed', decoded_token_response, 401)
            
        ####
        # auth_header = request.headers['access-token']
        # if auth_header:
        #     try:
        #         auth_token = auth_header.split(" ")[1]
        #         user_id = User.decode_auth_token(auth_token)
        #     except IndexError:
        #         return response('failed', 'Provide a valid auth token', 403)
        #     else:
        #         decoded_token_response = User.decode_auth_token(auth_token)
        #         if not isinstance(decoded_token_response, str):
        #             this_user = User.get_by_id(user_id)
        #             this_user.set_loggedin_false()
        #             token = BlackListToken(auth_token)
        #             token.blacklist()
        #             return response('success', 'Successfully logged out', 200)
        #         return response('failed', decoded_token_response, 401)
        # return response('failed', 'Provide an authorization header', 403)
