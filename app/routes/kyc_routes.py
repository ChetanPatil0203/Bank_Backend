from flask import Blueprint
from app.controllers.kyc_controller import KycController

kyc_bp = Blueprint('kyc_bp', __name__)

# User submitting KYC flow
@kyc_bp.route('/send-otp', methods=['POST'])
def send_kyc_otp():
    return KycController.send_kyc_otp()

@kyc_bp.route('/verify-otp', methods=['POST'])
def verify_kyc_otp():
    return KycController.verify_kyc_otp()

@kyc_bp.route('/submit', methods=['POST'])
def submit_kyc():
    return KycController.submit_kyc()

# Admin Management flow
@kyc_bp.route('/all', methods=['GET'])
def get_all_kycs():
    return KycController.get_all_kycs()

@kyc_bp.route('/<custom_id>/status', methods=['PUT'])
def update_kyc_status(custom_id):
    return KycController.update_kyc_status(custom_id)
