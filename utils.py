from functools import wraps
from flask import session, jsonify, request, url_for
from shop.config import App_Config
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
import time
from flask_mail import Message

def generate_verification_token(user_id):
    # Create a serializer with a secret key and an expiration time (in seconds)
    s = Serializer(App_Config.SECRET_KEY)  # Token expires in 1 hour

    # Create the token
    expiration_time = int(time.time()) + 86400
    token_data = {'user_id': user_id, "exp": expiration_time}
    token = s.dumps(token_data)
    return token

def verify_verification_token(token):
    s = Serializer(App_Config.SECRET_KEY)

    try:
        # Deserialize the token and extract the user_id as a string
        data = s.loads(token, max_age=3600)
        if time.time() <= data.get("exp", 0):
            user_id = data.get('user_id')
        else:
            raise Exception("Token has expired")

        return user_id
    except Exception as e:
        # Token is invalid or has expired
        return None

# Wrapper function to make sure the user is logged in
def login_is_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        jwt_token = request.headers.get('Authorization')

        if jwt_token:
            if jwt_token.startswith("Bearer "):
                token = jwt_token.split(' ')[1]
                try:
                    user_id = verify_verification_token(token)
                    if user_id:
                        return function(*args, **kwargs)
                    else:
                        return jsonify({"error": "Token is invalid"}), 401
                except jwt.ExpiredSignatureError:
                    return jsonify({"error": "Token has expired"}), 401
                except jwt.DecodeError:
                    return jsonify({"error": "Token is invalid"}), 401
        else:
            return jsonify({"error": "You are not logged in"}), 401

    return decorated_function

# Wrapper function to make sure the user is an admin
def admin_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        jwt_token = request.headers.get('Authorization')

        if not jwt_token:
            return jsonify({"error": "You are not logged in"}), 401

        if jwt_token.startswith("Bearer "):
            token = jwt_token.split(' ')[1]
            user_id = verify_verification_token(token)

            if user_id:
                user = Users.query.get(user_id)
                if not user:
                    return jsonify({"error": "User not found"}), 404
                if user.role == 'ADMIN':
                    return function(*args, **kwargs)

            return jsonify({"error": "Invalid or expired token"}), 401

    return decorated_function


def get_user():
    jwt_token = request.headers.get('Authorization')

    if not jwt_token:
        return jsonify({"Error": "Token is missing"}), 401

    if jwt_token.startswith("Bearer "):
        token = jwt_token.split(' ')[1]
        user_id = verify_verification_token(token)

        if user_id:
            user = Users.query.get(user_id)
            if not user:
                return jsonify({"Error": "User not found"}), 404
            return user

        return jsonify({"Error": "Invalid or expired token"}), 401

def generate_email_verification_token(email):
    s = Serializer(App_Config.SECRET_KEY)

    expiration_time = int(time.time()) + 86400  # 1 day
    token_data = {'email': email, "exp": expiration_time}
    token = s.dumps(token_data)
    return token

def verify_email_verification_token(token):
    s = Serializer(App_Config.SECRET_KEY)

    try:
        # Deserialize the token and extract the email
        data = s.loads(token, max_age=3600)
        if time.time() <= data.get("exp", 0):
            email = data.get('email')
            return email
        else:
            return jsonify({"Error":"Token has expired"}), 401
    except Exception as e:
        return jsonify({"Error": "Token is invalid or expired"}), 401

def send_verify_email(user):
    token = generate_email_verification_token(user.email)
    msg = Message("Verify email", sender='noreply@library.com', recipients=[user.email])
    msg.body = f"""To verify your email, visit the following link:
    {url_for('inApp.verify', token=token, _external=True)}

    If you did not make this request, simply ignore this message.
    """

    mail.send(msg)

def forgot_password(user):
    token = generate_email_verification_token(user.email)
    msg = Message("Reset password", sender='noreply@library.com', recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
    {url_for('inApp.reset', token=token, _external=True)}

    If you did not make this request, simply ignore this message.
    """

    mail.send(msg)
