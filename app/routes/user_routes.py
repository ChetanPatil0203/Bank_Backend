from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import AuthController

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/profile', methods=['GET', 'PUT', 'POST', 'OPTIONS'])
def manage_user_profile():
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    if request.method in ['PUT', 'POST']:
        return AuthController.update_profile()
    return AuthController.get_profile()

@user_bp.route('/account-status', methods=['GET', 'OPTIONS'])
def get_account_status():
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    return AuthController.get_account_status()
