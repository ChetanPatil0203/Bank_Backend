from flask import Flask
from flask_cors import CORS
from app.config.config import Config
from app.db import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)
    db.init_app(app)
    
    with app.app_context():
        # Import models so they are registered with SQLAlchemy
        from app.models.user_model import UserRegister, UserLogin
        
        # Automatically create database tables if they don't exist
        db.create_all()
        
        # Register Blueprints
        from app.routes.auth_routes import auth_bp
        # Uncomment other routes later
        # from app.routes.account_routes import account_bp
        
        app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
        # app.register_blueprint(account_bp, url_prefix='/api/v1/account')
        
    return app
