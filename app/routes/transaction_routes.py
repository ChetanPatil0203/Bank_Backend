from flask import Blueprint, request, jsonify
from app.controllers.transaction_controller import TransactionController

transaction_bp = Blueprint('transaction_bp', __name__)

@transaction_bp.route('/admin/transactions', methods=['POST', 'OPTIONS'])
def process_transaction():
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    return TransactionController.process_transaction()

@transaction_bp.route('/auth/transactions', methods=['GET', 'OPTIONS'])
def get_my_transactions():
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    return TransactionController.get_my_transactions()

@transaction_bp.route('/admin/txn-accounts', methods=['GET', 'OPTIONS'])
def get_admin_accounts():
    if request.method == 'OPTIONS':
        return jsonify({'success': True}), 200
    return TransactionController.get_admin_accounts()
