from flask import jsonify


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


def response_auth(status, message, token, status_code, username):
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
        'auth_token': token,
        'username': username}
    )

    response.headers['Authorization'] = token

    return response
