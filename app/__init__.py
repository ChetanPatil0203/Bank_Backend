import os
from flask import Flask, request
from flask_cors import CORS
from app.config.config import Config
from app.db import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS for frontend (React)
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}})
    db.init_app(app)
    
    with app.app_context():
        # Import models so they are registered with SQLAlchemy
        from app.models.user_model import UserRegister, UserLogin, PasswordReset, AdminLogin, UserPreference
        from app.models.account_model import AccountRequest, BankAccount
        from app.models.kyc_model import KYCSubmission
        from app.models.transaction_model import Transaction
        from app.models.support_model import SupportTicket, TicketMessage
        
        # Ensure upload folder exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
            
        db.create_all()

        # --- SEED ADMIN CREDENTIALS ---
        from werkzeug.security import generate_password_hash
        admin_email = "Payzen2026@gmail.com"
        admin_pass = "Payzen@2026"
        
        admin_exists = AdminLogin.query.filter_by(email=admin_email).first()
        if not admin_exists:
            new_admin = AdminLogin(
                email=admin_email,
                password_hash=generate_password_hash(admin_pass)
            )
            db.session.add(new_admin)
            db.session.commit()
            print(f"\n[INIT] Admin seeded: {admin_email}\n")
        # -----------------------------
        
        from app.routes.auth_routes import auth_bp
        from app.routes.account_routes import account_bp
        from app.routes.kyc_routes import kyc_bp
        from app.routes.user_routes import user_bp
        from app.routes.transaction_routes import transaction_bp
        from app.routes.ai_routes import ai_bp
        from app.routes.settings_routes import settings_bp
        from app.routes.support_routes import support_bp
        
        app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
        app.register_blueprint(account_bp, url_prefix='/api/v1')
        app.register_blueprint(kyc_bp, url_prefix='/api/v1/kyc')
        app.register_blueprint(user_bp, url_prefix='/api/v1/users')
        app.register_blueprint(transaction_bp, url_prefix='/api/v1')
        app.register_blueprint(ai_bp, url_prefix='/api/v1/ai')
        app.register_blueprint(settings_bp, url_prefix='/api/v1/settings')
        app.register_blueprint(support_bp, url_prefix='/api/v1/support')

        
        @app.before_request
        def log_request():
            print(f">>> REQ: {request.method} {request.path} {request.args} <<<")
        
        print("\nRegistered Routes:")
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint}: {rule.rule}")
        print("\n")
        
    return app