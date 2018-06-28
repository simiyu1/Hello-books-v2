from flask import request, make_response, jsonify
from app.user.models import User
from functools import wraps


def token_required(f):
    """
    Decorator function to ensure that a resource is access by only authenticated users`
    provided their auth tokens are valid
    :param f:
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return {
                    'status': 'failed',
                    'message': 'Provide a valid auth token'
                }

        if not token:
            return {
                'status': 'failed',
                'message': 'Token is missing'
            }

        try:
            decode_response = User.decode_auth_token(token)
            current_user = User.query.filter_by(id=decode_response).first()
        except:
            message = 'Invalid token'
            if isinstance(decode_response, str):
                message = decode_response
            return {
                'status': 'failed',
                'message': message
            }

        return f(current_user, *args, **kwargs)

    return decorated_function


def response(status, message, status_code):
    """
    Helper method to make an Http response
    :param status: Status
    :param message: Message
    :param status_code: Http status code
    :return:
    """
    return {
        'status': status,
        'message': message
    }


def response_auth(status, message, token, status_code):
    """
    Make a Http response to send the auth token
    :param status: Status
    :param message: Message
    :param token: Authorization Token
    :param status_code: Http status code
    :return: Http Json response
    """
    response = jsonify({
        'status': status,
        'message': message,
        'auth_token': token}
    )

    response.headers['Authorization'] = token

    return response
