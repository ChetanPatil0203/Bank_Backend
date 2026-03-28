from flask import Blueprint, jsonify, request
from app.controllers.account_controller import AccountController

account_bp = Blueprint('account_bp', __name__)

@account_bp.route('/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({'success': True, 'message': 'Backend is alive!'}), 200

# User Routes
@account_bp.route('/accounts/open-request', methods=['POST', 'OPTIONS'])
def open_account():
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    return AccountController.submit_request()

# Admin Routes — Supporting both common endpoint names for compatibility
@account_bp.route('/admin/requests', methods=['GET', 'POST', 'OPTIONS'])
@account_bp.route('/admin/account-requests', methods=['GET', 'OPTIONS'])
def manage_requests():
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    if request.method == 'POST':
        return AccountController.submit_request()
    return AccountController.get_requests()

@account_bp.route('/admin/requests/<int:id>/approve', methods=['POST', 'OPTIONS'])
@account_bp.route('/admin/account-requests/<int:id>/approve', methods=['POST', 'OPTIONS'])
def approve_request(id):
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    return AccountController.approve_request(id)

@account_bp.route('/admin/requests/<int:id>/reject', methods=['POST', 'OPTIONS'])
@account_bp.route('/admin/account-requests/<int:id>/reject', methods=['POST', 'OPTIONS'])
def reject_request(id):
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    return AccountController.reject_request(id)

@account_bp.route('/admin/uploads/<path:filename>', methods=['GET'])
def serve_upload(filename):
    from flask import send_from_directory, current_app
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@account_bp.route('/admin/accounts', methods=['GET', 'OPTIONS'])
def get_accounts():
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    return AccountController.get_accounts()

@account_bp.route('/admin/accounts/<int:id>/toggle', methods=['POST', 'OPTIONS'])
def toggle_status(id):
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    return AccountController.toggle_status(id)

@account_bp.route('/admin/accounts/<int:id>/close', methods=['POST', 'OPTIONS'])
def close_account(id):
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    return AccountController.close_account(id)
