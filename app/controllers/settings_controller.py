from flask import request, jsonify
from app.services.settings_service import SettingsService
from app.utils import decode_jwt_token

class SettingsController:

    @staticmethod
    def _get_user_id():
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        token = auth_header.split(" ")[1]
        decoded = decode_jwt_token(token)
        if not decoded:
            return None
        
        return decoded.get('user_id')

    @staticmethod
    def get_profile():
        user_id = SettingsController._get_user_id()
        if not user_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        
        result = SettingsService.get_profile(user_id)
        return jsonify(result), 200 if result.get('success') else 400

    @staticmethod
    def update_profile():
        user_id = SettingsController._get_user_id()
        if not user_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        
        data = request.get_json()
        result = SettingsService.update_profile(user_id, data)
        return jsonify(result), 200 if result.get('success') else 400

    @staticmethod
    def get_preferences():
        user_id = SettingsController._get_user_id()
        if not user_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        
        result = SettingsService.get_preferences(user_id)
        return jsonify(result), 200 if result.get('success') else 400

    @staticmethod
    def update_preferences():
        user_id = SettingsController._get_user_id()
        if not user_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        
        data = request.get_json()
        result = SettingsService.update_preferences(user_id, data)
        return jsonify(result), 200 if result.get('success') else 400

    @staticmethod
    def change_password():
        user_id = SettingsController._get_user_id()
        if not user_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        
        data = request.get_json()
        result = SettingsService.change_password(user_id, data)
        return jsonify(result), 200 if result.get('success') else 400

    @staticmethod
    def get_activity():
        user_id = SettingsController._get_user_id()
        if not user_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        
        result = SettingsService.get_login_activity(user_id)
        return jsonify(result), 200 if result.get('success') else 400
