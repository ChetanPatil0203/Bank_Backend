from app.models.user_model import UserRegister, UserLogin
from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from flask import current_app

class AuthService:
    @staticmethod
    def register_user(data):
        email = data.get('email')
        
        # Check if user already exists in login table
        existing_user = UserLogin.query.filter_by(email=email).first()
        if existing_user:
            return {'success': False, 'message': 'Email already registered.'}
            
        password = data.get('password')
        confirm_password = data.get('confirmPassword')
        
        if password != confirm_password:
            return {'success': False, 'message': 'Passwords do not match.'}
        
        hashed_password = generate_password_hash(password)
        
        try:
            dob_str = data.get('date_of_birth')
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None
            
            # Save strictly personal details to register table
            new_register = UserRegister(
                name=data.get('name'),
                email=email,
                mobile=data.get('mobile'),
                date_of_birth=dob,
                gender=data.get('gender')
            )
            
            # Save credentials to separated login table
            new_login = UserLogin(
                email=email,
                password_hash=hashed_password
            )
            
            db.session.add(new_register)
            db.session.add(new_login)
            db.session.commit()
            
            return {'success': True, 'message': 'User registered successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Server error: {str(e)}'}

    @staticmethod
    def login_user(data):
        email = data.get('email')
        password = data.get('password')
        
        # Query the separate login table for secure verification
        user_login = UserLogin.query.filter_by(email=email).first()
        
        if not user_login or not check_password_hash(user_login.password_hash, password):
            return {'success': False, 'message': 'Invalid Credentials!'}
            
        user_register = UserRegister.query.filter_by(email=email).first()
        
        try:
            token = jwt.encode({
                'user_id': user_login.id,
                'email': user_login.email,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, current_app.config['SECRET_KEY'], algorithm='HS256')
            
            # Save the generated JWT token to the login table
            user_login.jwt_token = token
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Login Successful! 🎉',
                'user': user_register.to_dict() if user_register else {'email': user_login.email, 'id': user_login.id},
                'token': token
            }
        except Exception as e:
            return {'success': False, 'message': f'Error generating token: {str(e)}'}
