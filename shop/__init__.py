from flask import Flask, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from shop.config import App_Config
from flask_dance.contrib.github import make_github_blueprint, github
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_mail import Mail


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(App_Config)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    
    # import blueprints
    from shop.oauth.github.routes import github_bp
    from shop.oauth.google.routes import auth
    from shop.oauth.inApp.routes import inapp_bp
    from shop.category.routes import category_bp
    from shop.buyer.routes import buyer_bp
    from shop.product.routes import product_bp

    #register blueprints
    app.register_blueprint(github_bp, url_prefix='/api/github')
    app.register_blueprint(auth)
    app.register_blueprint(inapp_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(buyer_bp)
    app.register_blueprint(product_bp)

    # Initialize CORS
    CORS(app, supports_credentials=True)

    # Configure swagger UI
    SWAGGER_URL = '/api/apidocs'
    API_URL = '/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Shop"}
    )

    @app.route('/swagger.json')
    def swagger():
        with open('swagger.json', 'r') as f:
            return jsonify(json.load(f))

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
