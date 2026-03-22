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
        from app.models.user_model import UserRegister, UserLogin, PasswordReset  # ✅ PasswordReset added
        
        
        db.create_all()
        
        from app.routes.auth_routes import auth_bp
        
        
        app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
       
        
    return app