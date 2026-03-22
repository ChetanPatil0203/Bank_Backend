from flask import request, jsonify
from app.services.auth_service import AuthService

class AuthController:

    # ─── REGISTER ─────────────────────────────────────────────────────────────
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

    # ─── LOGIN ────────────────────────────────────────────────────────────────
    @staticmethod
    def login():
        data = request.get_json()

        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'message': 'Email and Password required.'}), 400

        result = AuthService.login_user(data)
        status_code = 200 if result.get('success') else 401
        return jsonify(result), status_code

    # ─── FORGOT — STEP 1: Send OTP ────────────────────────────────────────────
    @staticmethod
    def forgot_send_otp():
        data = request.get_json()
        if not data or not data.get('email'):
            return jsonify({'success': False, 'message': 'Email is required.'}), 400

        result = AuthService.forgot_send_otp(data.get('email').strip().lower())
        status_code = 200 if result.get('success') else 404
        return jsonify(result), status_code

    # ─── FORGOT — STEP 2: Verify OTP ──────────────────────────────────────────
    @staticmethod
    def forgot_verify_otp():
        data = request.get_json()
        if not data or not data.get('email') or not data.get('otp'):
            return jsonify({'success': False, 'message': 'Email and OTP required.'}), 400

        result = AuthService.forgot_verify_otp(
            data.get('email').strip().lower(),
            data.get('otp').strip()
        )
        status_code = 200 if result.get('success') else 400
        return jsonify(result), status_code

    # ─── FORGOT — STEP 3: Reset Password ──────────────────────────────────────
    @staticmethod
    def forgot_reset_password():
        data = request.get_json()
        password = data.get('newPass') or data.get('new_password') or data.get('password')
        
        if not data or not data.get('email') or not password:
            return jsonify({'success': False, 'message': 'Email and new password required.'}), 400

        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters.'}), 400

        result = AuthService.forgot_reset_password(
            data.get('email').strip().lower(),
            password
        )
        status_code = 200 if result.get('success') else 400
        return jsonify(result), status_code

    # ─── LOGOUT ────────────────────────────────────────────────────────────────
    @staticmethod
    def logout():
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({'success': False, 'message': 'Missing or Invalid Token'}), 401
        
        token = auth_header.split(" ")[1]
        result = AuthService.logout_user(token)
        status_code = 200 if result.get('success') else 400
        return jsonify(result), status_code