from flask import request, jsonify
from app.services.auth_service import AuthService

class AuthController:
    @staticmethod
    def register():
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No data provided.'}), 400
            
        required_fields = ['name', 'email', 'mobile', 'date_of_birth', 'gender', 'password', 'confirmPassword']
        for field in required_fields:
            if field not in data or not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required.'}), 400
                
        result = AuthService.register_user(data)
        
        status_code = 201 if result.get('success') else 400
        return jsonify(result), status_code

    @staticmethod
    def login():
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'message': 'Email and Password required.'}), 400
            
        result = AuthService.login_user(data)
        
        status_code = 200 if result.get('success') else 401
        return jsonify(result), status_code
