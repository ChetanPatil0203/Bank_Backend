from flask import request, jsonify
from app.services.account_service import AccountService

class AccountController:

    @staticmethod
    def submit_request():
        if request.method == 'OPTIONS':
            return jsonify({'success': True}), 200
            
        # Handle both JSON and Form Data
        print(f">>> CONTROLLER: Request Content-Type: {request.content_type} <<<")
        print(f">>> CONTROLLER: Request Files: {request.files.keys()} <<<")
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        files = request.files
        
        print(">>> CONTROLLER: Incoming data:", data, "<<<")
        
        if not data:
            return jsonify({'success': False, 'message': 'No data provided.'}), 400
            
        required_fields = ['bank_holder_name', 'email', 'mobile', 'aadhaar', 'pan', 'account_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required.'}), 400
        
        result = AccountService.submit_request(data, files)
        print("Submission result:", result)
        status_code = 201 if result.get('success') else 400
        return jsonify(result), status_code

    @staticmethod
    def get_requests():
        print(">>> [GET] ADMIN REQUESTS CALLED <<<")
        result = AccountService.get_all_requests()
        print(f">>> Returning {len(result.get('data', []))} records to Frontend <<<")
        return jsonify(result.get('data', [])), 200

    @staticmethod
    def get_request_details(id):
        return jsonify(AccountService.get_request_by_id(id)), 200

    @staticmethod
    def approve_request(id):
        result = AccountService.approve_request(id)
        status_code = 200 if result.get('success') else 400
        return jsonify(result), status_code

    @staticmethod
    def reject_request(id):
        result = AccountService.reject_request(id)
        status_code = 200 if result.get('success') else 400
        return jsonify(result), status_code

    @staticmethod
    def get_accounts():
        query = request.args.get('search', '')
        result = AccountService.get_all_accounts(query)
        # Return only the data list so the frontend can correctly parse it as an array
        return jsonify(result.get('data', [])), 200

    @staticmethod
    def toggle_status(id):
        result = AccountService.toggle_status(id)
        status_code = 200 if result.get('success') else 400
        return jsonify(result), status_code

    @staticmethod
    def close_account(id):
        result = AccountService.close_account(id)
        status_code = 200 if result.get('success') else 400
        return jsonify(result), status_code
