from flask import Blueprint, jsonify, request
from shop.models.users import Users
from shop import db, bcrypt
from utils import send_verify_email, verify_email_verification_token, generate_verification_token, login_is_required, forgot_password


inapp_bp = Blueprint('inApp', __name__, url_prefix='/api/oauth')

@inapp_bp.route("/signup", methods=['POST'])
def signup():
    limiter = request.view_args['limiter']
    data = request.get_json()
    required_attributes = ['name', 'email', 'password', 'confirm_password']

    if not all(attr in data for attr in required_attributes):
        return jsonify({"error": "Missing or incorrect data in the request"}), 400

    if data['password'] != data['confirm_password']:
        return jsonify({"error": "Passwords do not match"}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = Users(name=data['name'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit() 

    send_verify_email(user)

    return jsonify({"message": "Verification email sent"}), 200

@inapp_bp.route("/verify/<string:token>")
def verify(token):
    email = verify_email_verification_token(token)

    if email is not None:
        user = Users.query.filter_by(email=email).first()
        if user:
            user.is_active = True
            db.session.commit()
            return jsonify({"message": "Email verified successfully"}), 200
        return jsonify({"error": "User not found"}), 404

    return jsonify({"error": "Invalid or expired token"}), 400

@inapp_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    required_attributes = ['email', 'password']

    if not all(attr in data for attr in required_attributes):
        return jsonify({"error": "Missing or incorrect data in the request"}), 400

    user = Users.query.filter_by(email=data['email']).first()
    if user:
        if bcrypt.check_password_hash(user.password, data['password']):
            user.token = generate_verification_token(user.id)
            db.session.commit()
            return jsonify({"message": f"{user.name} logged in"}), 200
        return jsonify({"error": "Passwords do not match"}), 401
    return jsonify({"error": "User not found"}), 404

@inapp_bp.route("/forgot_password", methods=['POST'])
def forgot_password():
    data = request.get_json()
    if 'email' not in data or data['email'] is None or data['email'] == "":
        return jsonify({"Error": "Supply your email address"}), 400

    user = Users.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"Success": "The email address you supplied is not registered"}), 400

    forgot_password(user)
    return jsonify({"message": "an email has been sent to your email address"}), 200
    

@inapp_bp.route("/reset/<string:token>", methods=['POST'])
def reset(token):
    email = verify_email_verification_token(token)
    data = request.get_json()
    allowed_attributes = ['password', 'confirm_password']

    if not all(attr in data for attr in allowed_attributes):
        return jsonify({"error": "Missing or incorrect data in the request"}), 400

    if data['password'] != data['confirm_password']:
        return jsonify({"Error": "Passwords do not match"}), 401

    if email is not None:
        user = Users.query.filter_by(email=email).first()
        if user:
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

            return jsonify({"Success": "Password updated successfully"}), 200

        return jsonify({"Error": "User not found"}), 404
    return jsonify({"Error": "invalid or expired token"}), 400
