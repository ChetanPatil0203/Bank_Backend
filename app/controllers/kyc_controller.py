from flask import request, jsonify, current_app
from app.services.kyc_service import KycService

class KycController:
    # ─── SEND OTP ────────────────────────────────────────────────────────────
    @staticmethod
    def send_kyc_otp():
        data = request.get_json()
        if not data or not data.get('email'):
            return jsonify({'success': False, 'message': 'Email is required.'}), 400

        result = KycService.send_kyc_otp(data.get('email'))
        status_code = 200 if result.get('success') else 400
        return jsonify(result), status_code

    # ─── VERIFY OTP ──────────────────────────────────────────────────────────
    @staticmethod
    def verify_kyc_otp():
        data = request.get_json()
        email = data.get('email')
        otp = data.get('otp')

        if not email or not otp:
            return jsonify({'success': False, 'message': 'Email and OTP required.'}), 400

        result = KycService.verify_kyc_otp(email, otp)
        status_code = 200 if result.get('success') else 400
        return jsonify(result), status_code

    # ─── SUBMIT KYC ──────────────────────────────────────────────────────────
    @staticmethod
    def submit_kyc():
        # Using form data cause files are uploaded
        data = request.form.to_dict()
        files = request.files

        required_fields = ['fullName', 'email', 'mobile', 'dob', 'address', 'aadhaar', 'pan']
        for field in required_fields:
            if field not in data or not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required.'}), 400

        upload_folder = current_app.config['UPLOAD_FOLDER']
        result = KycService.submit_kyc(data, files, upload_folder)
        
        status_code = 201 if result.get('success') else 400
        return jsonify(result), status_code

    # ─── GET ALL KYCs (Admin) ────────────────────────────────────────────────
    @staticmethod
    def get_all_kycs():
        result = KycService.get_all_kycs()
        status_code = 200 if result.get('success') else 500
        return jsonify(result), status_code

    # ─── UPDATE KYC STATUS (Admin) ───────────────────────────────────────────
    @staticmethod
    def update_kyc_status(custom_id):
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'success': False, 'message': 'Status is required.'}), 400
            
        status = data.get('status')
        reason = data.get('rejectReason')
        
        result = KycService.update_kyc_status(custom_id, status, reason)
        status_code = 200 if result.get('success') else 400
        return jsonify(result), status_code
