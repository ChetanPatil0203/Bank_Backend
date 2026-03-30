from app.models.account_model import BankAccount
from app.models.user_model import UserLogin, UserRegister
from app.models.transaction_model import Transaction
from app.db import db
from sqlalchemy import or_

class TransactionService:
    @staticmethod
    def get_admin_accounts(query=""):
        try:
            query = query.strip()
            print(f"DEBUG: Searching accounts with query: '{query}'")
            # We want to fetch all bank accounts and optionally filter by query
            accounts = BankAccount.query
            if query:
                # Replace spaces with % to handle multiple spaces in DB
                search = f"%{query.replace(' ', '%')}%"
                print(f"DEBUG: SQL Search pattern: '{search}'")
                accounts = accounts.filter(
                    or_(
                        BankAccount.bank_holder_name.ilike(search),
                        BankAccount.account_number.ilike(search)
                    )
                )
            
            accounts = accounts.all()
            print(f"DEBUG: Found {len(accounts)} accounts.")
            for acc in accounts:
                print(f"DEBUG Account Found: {acc.bank_holder_name} ({acc.account_number})")

            return {'success': True, 'data': [acc.to_dict() for acc in accounts]}
        except Exception as e:
            print(f"DEBUG ERROR in get_admin_accounts: {str(e)}")
            return {'success': False, 'message': f'Error fetching accounts: {str(e)}'}

    @staticmethod
    def perform_transaction(token, data):
        # We need to verify if the token belongs to an Admin (optional, depending on auth setup)
        # But here we'll assume the route allows it or token check is sufficient
        try:
            user_login = UserLogin.query.filter_by(jwt_token=token).first()
            if not user_login:
                return {'success': False, 'message': 'Unauthorized', 'isAuth': False}

            account_number = data.get('account_number')
            txn_type = data.get('type') # 'Deposit' or 'Withdraw'
            amount = data.get('amount')
            note = data.get('note', '')

            if not account_number or not txn_type or amount is None:
                return {'success': False, 'message': 'Missing required fields (account_number, type, amount).'}

            amount = float(amount)
            if amount <= 0:
                return {'success': False, 'message': 'Amount must be greater than zero.'}

            if txn_type not in ['Deposit', 'Withdraw']:
                return {'success': False, 'message': "Invalid transaction type. Must be 'Deposit' or 'Withdraw'."}

            account = BankAccount.query.filter_by(account_number=account_number).first()
            if not account:
                return {'success': False, 'message': 'Account not found.'}

            if account.status == 'Closed':
                return {'success': False, 'message': 'Cannot perform transaction on a closed account.'}

            if txn_type == 'Withdraw':
                if float(account.balance) < amount:
                    return {'success': False, 'message': 'Insufficient balance for withdrawal.'}
                account.balance = float(account.balance) - amount
            else:
                account.balance = float(account.balance) + amount

            # Create Transaction Record
            new_txn = Transaction(
                account_id=account.id,
                account_number=account.account_number,
                user_name=account.bank_holder_name,
                type=txn_type,
                amount=amount,
                note=note,
                status='Success'
            )

            db.session.add(new_txn)
            db.session.commit()

            return {
                'success': True, 
                'message': f'{txn_type} successful!', 
                'data': {
                    'account': account.to_dict(),
                    'transaction': new_txn.to_dict()
                }
            }

        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Transaction failed: {str(e)}'}

    @staticmethod
    def get_user_transactions(token):
        try:
            user_login = UserLogin.query.filter_by(jwt_token=token).first()
            if not user_login:
                return {'success': False, 'message': 'Unauthorized', 'isAuth': False}
                
            email = user_login.email
            register = UserRegister.query.filter_by(email=email).first()
            if not register:
                return {'success': False, 'message': 'User profile not found.'}

            # Find the bank account associated with this user
            from app.models.account_model import AccountRequest
            account_request = AccountRequest.query.filter_by(email=email, status='Approved').order_by(AccountRequest.created_at.desc()).first()
            
            if not account_request:
                return {'success': True, 'data': {'account_number': None, 'balance': 0, 'transactions': []}}

            bank_account = BankAccount.query.filter_by(request_id=account_request.id).first()
            if not bank_account:
                return {'success': True, 'data': {'account_number': None, 'balance': 0, 'transactions': []}}

            transactions = Transaction.query.filter_by(account_id=bank_account.id).order_by(Transaction.created_at.desc()).all()

            return {
                'success': True, 
                'data': {
                    'account_number': bank_account.account_number,
                    'balance': float(bank_account.balance),
                    'transactions': [txn.to_dict() for txn in transactions]
                }
            }

        except Exception as e:
            return {'success': False, 'message': f'Error fetching transactions: {str(e)}'}
