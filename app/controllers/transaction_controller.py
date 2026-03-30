from flask import request, jsonify
from app.services.transaction_service import TransactionService

class TransactionController:
    @staticmethod
    def get_admin_accounts():
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({'success': False, 'message': 'Missing or Invalid Token'}), 401
        
        query = request.args.get('search', '')
        result = TransactionService.get_admin_accounts(query)
        status = 200 if result.get('success') else 400
        return jsonify(result), status

    @staticmethod
    def process_transaction():
        auth_header = request.headers.get("Authorization")
        print(f"DEBUG: Transaction Controller received Auth Header: {auth_header}")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({'success': False, 'message': 'Missing Token', 'isAuth': False}), 401
        
        token = auth_header.split(" ")[1]
        data = request.get_json() or {}
        print(f"DEBUG: Processing transaction for data: {data}")
        
        result = TransactionService.perform_transaction(token, data)
        status = 200 if result.get('success') else (401 if 'isAuth' in result else 400)
        return jsonify(result), status

    @staticmethod
    def get_my_transactions():
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({'success': False, 'message': 'Missing Token', 'isAuth': False}), 401
        
        token = auth_header.split(" ")[1]
        result = TransactionService.get_user_transactions(token)
        
        status = 200 if result.get('success') else (401 if 'isAuth' in result else 400)
        return jsonify(result), status
