from app import app, db, bcrypt
from flask import jsonify
import datetime
import jwt


class User(db.Model):
    """

    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    logged_in = db.Column(db.Boolean, default=False, nullable=False)
    role = db.Column(db.String(50), default="normal", nullable=False)
    
    def __init__(self, email, password, username):
        self.email = email
        self.username = username
        self.password = bcrypt.generate_password_hash(password, app.config.get('BCRYPT_LOG_ROUNDS')) \
            .decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.logged_in = False

    def save(self):
        """
        Persist the user in the database
        :param user:
        :return:
        """
        db.session.add(self)
        db.session.commit()
        return self.encode_auth_token(self.id)

    def encode_auth_token(self, user_id):
        """
        Encode the Auth token
        :param user_id: User's Id
        :return:
        """

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=app.config.get('AUTH_TOKEN_EXPIRY_DAYS'),
                                                                       seconds=app.config.get(
                                                                           'AUTH_TOKEN_EXPIRY_SECONDS')),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            p = jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            self.logged_in = True
            db.session.add(self)
            db.session.commit()
            return p.decode("UTF-8")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(token):
        """
        Decoding the token to get the payload and then return the user Id in 'sub'
        :param token: Auth Token
        :return:
        """
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            is_token_blacklisted = BlackListToken.check_blacklist(token)
            if is_token_blacklisted:
                return 'Token was Blacklisted, Please login In'
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired, Please sign in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please sign in again'

    @staticmethod
    def get_by_id(user_id):
        """
        Get a single user entry by ID.
        :param user_id:
        :return: User or None
        """
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_many():
        """
        return all users
        :param: blank
        :return: Users or None
        """
        results = User.query.filter().paginate(1, 10, True)
        itemized = results.items
        return jsonify({
            "page": results.page,
            "total_results": results.total,
            "total_pages": results.pages,
            "per_page": results.per_page,
            "objects": [{'id': User.id, 'username': User.username,
                         'email': User.email, 'Role': User.role, 'Logged in': User.logged_in
                         } for User in itemized
                        ]}, {"message": "Returns all users"})

    @staticmethod
    def get_by_email(email):
        """
        Get a single user entry by their email address
        :param email:
        :return: User or None
        """
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_username(username):
        """
        Check a user by their email address
        :param email:
        :return: User or None
        """
        return User.query.filter_by(username=username).first()

    def reset_password(self, new_password):
        """
        Update/reset the user password.
        :param new_password: New User Password
        :return:
        """
        self.password = bcrypt.generate_password_hash(new_password, app.config.get('BCRYPT_LOG_ROUNDS')) \
            .decode('utf-8')
        db.session.commit()

    def set_loggedin_false(self):
        """
        Change Boolean Logged in to false
        :param user:
        :return:None
        """
        self.logged_in = False
        db.session.add(self)
        db.session.commit()

    def make_admin(self):
        """
        Elevate user privileges
        :param user:
        :return:None
        """
        self.role = 'admin'
        db.session.add(self)
        db.session.commit()
        return self.encode_auth_token(self.id)


class BlackListToken(db.Model):
    """
    Table to store blacklisted/invalid auth tokens
    """
    __tablename__ = 'blacklist_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def blacklist(self):
        """
        Persist Blacklisted token in the database
        :return:
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_blacklist(token):
        """
        Check to find out whether a token has already been blacklisted.
        :param token: Authorization token
        :return:
        """
        response = BlackListToken.query.filter_by(token=token).first()
        if response:
            return True
        return False
