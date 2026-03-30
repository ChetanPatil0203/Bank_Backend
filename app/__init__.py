import os
from flask import Flask
from flask_cors import CORS
from app.config.config import Config
from app.db import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS for all routes and origins
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    
    with app.app_context():
        # Import models so they are registered with SQLAlchemy
        from app.models.user_model import UserRegister, UserLogin, PasswordReset
        from app.models.account_model import AccountRequest, BankAccount
        from app.models.kyc_model import KYCSubmission
        from app.models.transaction_model import Transaction
        
        
        # Ensure upload folder exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
            
        db.create_all()
        
        from app.routes.auth_routes import auth_bp
        from app.routes.account_routes import account_bp
        from app.routes.kyc_routes import kyc_bp
        from app.routes.user_routes import user_bp
        from app.routes.transaction_routes import transaction_bp
        
        app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
        app.register_blueprint(account_bp, url_prefix='/api/v1')
        app.register_blueprint(kyc_bp, url_prefix='/api/v1/kyc')
        app.register_blueprint(user_bp, url_prefix='/api/v1/users')
        app.register_blueprint(transaction_bp, url_prefix='/api/v1')
       
        print("\nRegistered Routes:")
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint}: {rule.rule}")
        print("\n")
        
    return app