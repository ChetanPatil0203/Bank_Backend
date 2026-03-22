from flask import Blueprint
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint('auth_bp', __name__)

# ── Existing routes (unchanged) ──────────────────────────────────────────────
@auth_bp.route('/register', methods=['POST'])
def register():
    return AuthController.register()

@auth_bp.route('/login', methods=['POST'])
def login():
    return AuthController.login()

# ── Forgot Password — 3 steps ─────────────────────────────────────────────────
@auth_bp.route('/send-otp', methods=['POST'])
def forgot_send_otp():
    return AuthController.forgot_send_otp()

@auth_bp.route('/verify-otp', methods=['POST'])
def forgot_verify_otp():
    return AuthController.forgot_verify_otp()

@auth_bp.route('/reset-password', methods=['POST'])
def forgot_reset_password():
    return AuthController.forgot_reset_password()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return AuthController.logout()