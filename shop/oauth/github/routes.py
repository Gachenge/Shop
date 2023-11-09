from flask_dance.contrib.github import make_github_blueprint, github
from shop.config import App_Config
from flask import redirect, url_for, jsonify
from utils import generate_verification_token

github_bp = make_github_blueprint(client_id=App_Config.GITHUB_OAUTH_CLIENT_ID,
                                  client_secret=App_Config.
                                  GITHUB_OAUTH_CLIENT_SECRET)

@github_bp.route('/')
def github_login():
    """
    Allow users to log in via GitHub OAuth.
    """
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
        if account_info.ok:
            account_info_json = account_info.json()
            user = Users.query.filter_by(email=account_info_json['email']).first()

            if not user:
                user = Users(name=account_info_json['name'],
                             email=account_info_json['email'],
                             avatar=account_info_json['avatar_url'],)
                db.session.add(user)
                db.session.commit()
            jwt_token = generate_verification_token(user.id)
            user.token = jwt_token
            user.is_active = True
            db.session.commit()
        return jsonify({"Success": f"Welcome {user.name}"})
    return ({"Error": "User not authorised"}), 401
