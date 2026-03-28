import os
import uuid
import random
import string
from datetime import datetime
from werkzeug.utils import secure_filename
from app.models.account_model import AccountRequest, BankAccount
from app.db import db
from flask import current_app

class AccountService:

    @staticmethod
    def submit_request(data, files):
        try:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            print("--- Submit Request Detail ---")
            print(f"Current Working Dir: {os.getcwd()}")
            print(f"Upload Folder: {upload_folder}")
            print(f"Upload Folder Exists: {os.path.exists(upload_folder)}")
            print(f"Data fields: {data.keys()}")
            print(f"Files received: {files.keys()}")
            for k, v in files.items():
                print(f"File key: {k}, Filename: {getattr(v, 'filename', 'No filename')}, Type: {type(v)}")
            
            # Process files
            photo = files.get('photo')
            aadhaar_doc = files.get('aadhaarDoc') or files.get('aadhaar') or files.get('aadhaar_doc')
            pan_doc = files.get('panDoc') or files.get('pan') or files.get('pan_doc')
            
            paths = {}
            for key, file in [('photo', photo), ('aadhaar', aadhaar_doc), ('pan', pan_doc)]:
                if file:
                    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    paths[f"{key}_path"] = filename # Store only filename for easy access via static URL
            
            # Map common frontend field names to backend names
            mappings = {
                'name': 'bank_holder_name',
                'full_name': 'bank_holder_name',
                'phone': 'mobile',
                'type': 'account_type',
                'address_line1': 'address',
                'preferred_branch': 'branch',
                'signature': 'signature_name'
            }
            for frontend_key, backend_key in mappings.items():
                if frontend_key in data and not data.get(backend_key):
                    data[backend_key] = data[frontend_key]

            required_fields = ['bank_holder_name', 'dob', 'gender', 'mobile', 'email', 'address', 'aadhaar', 'pan', 'account_type', 'branch']
            for field in required_fields:
                if not data.get(field):
                    return {'success': False, 'message': f'Missing required field: {field}'}

            # Check if Aadhar already exists
            existing_request = AccountRequest.query.filter_by(aadhaar=data.get('aadhaar')).first()
            if existing_request:
                if existing_request.status == 'Approved':
                    return {'success': False, 'message': 'already account open'}
                elif existing_request.status == 'Pending':
                    return {'success': False, 'message': 'You already have a pending account request.'}
                else:
                    return {'success': False, 'message': 'already account open'}

            # Flexible date parsing
            dob_str = data.get('dob')
            dob = None
            if dob_str:
                for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y'):
                    try:
                        dob = datetime.strptime(dob_str, fmt).date()
                        break
                    except ValueError:
                        continue
                if not dob:
                    return {'success': False, 'message': f'Invalid date format for dob: {dob_str}'}
            
            new_request = AccountRequest(
                bank_holder_name=data.get('bank_holder_name'),
                father_name=data.get('father_name'),
                dob=dob,
                gender=data.get('gender'),
                mobile=data.get('mobile'),
                email=data.get('email'),
                address=data.get('address'),
                aadhaar=data.get('aadhaar'),
                pan=data.get('pan'),
                account_type=data.get('account_type'),
                branch=data.get('branch'),
                nominee_name=data.get('nominee_name'),
                nominee_relation=data.get('nominee_relation'),
                signature_name=data.get('signature_name'),
                reason=data.get('reason'),
                photo_path=paths.get('photo_path'),
                aadhaar_path=paths.get('aadhaar_path'),
                pan_path=paths.get('pan_path')
            )
            
            db.session.add(new_request)
            db.session.commit()
            
            return {'success': True, 'message': 'Account request submitted successfully. Waiting for admin approval.', 'data': new_request.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Error submitting request: {str(e)}'}

    @staticmethod
    def get_all_requests():
        try:
            print(">>> SERVICE: Fetching all requests from DB... <<<")
            requests = AccountRequest.query.order_by(AccountRequest.created_at.desc()).all()
            print(f">>> SERVICE: Found {len(requests)} account requests in DB <<<")
            return {'success': True, 'data': [r.to_dict() for r in requests]}
        except Exception as e:
            print(f">>> SERVICE ERROR: {e} <<<")
            return {'success': False, 'message': str(e), 'data': []}

    @staticmethod
    def get_request_by_id(request_id):
        return AccountRequest.query.get(request_id)

    @staticmethod
    def approve_request(request_id):
        try:
            req = AccountRequest.query.get(request_id)
            if not req:
                return {'success': False, 'message': 'Request not found.'}
            
            if req.status != 'Pending':
                return {'success': False, 'message': f'Request is already {req.status}.'}
            
            # Generate Account Number (12 digits)
            acc_num = "".join(random.choices(string.digits, k=12))
            while BankAccount.query.filter_by(account_number=acc_num).first():
                acc_num = "".join(random.choices(string.digits, k=12))
            
            ifsc = "PYZN0001" # Default IFSC for now
            
            new_account = BankAccount(
                account_number=acc_num,
                ifsc=ifsc,
                account_type=req.account_type,
                bank_holder_name=req.bank_holder_name,
                branch=req.branch, # Copy branch from request
                balance=0.00,
                status='Active',
                request_id=req.id
            )
            
            req.status = 'Approved'
            db.session.add(new_account)
            db.session.commit()
            
            return {
                'success': True, 
                'message': 'Account approved and created successfully.',
                'data': new_account.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Error approving request: {str(e)}'}

    @staticmethod
    def reject_request(request_id):
        try:
            req = AccountRequest.query.get(request_id)
            if not req:
                return {'success': False, 'message': 'Request not found.'}
            
            req.status = 'Rejected'
            db.session.commit()
            return {'success': True, 'message': 'Account request rejected.'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Error rejecting request: {str(e)}'}

    @staticmethod
    def get_all_accounts():
        try:
            accounts = BankAccount.query.order_by(BankAccount.opened_at.desc()).all()
            return {'success': True, 'data': [a.to_dict() for a in accounts]}
        except Exception as e:
            return {'success': False, 'message': str(e), 'data': []}

    @staticmethod
    def toggle_account_status(account_id):
        try:
            acc = BankAccount.query.get(account_id)
            if not acc or acc.status == 'Closed':
                return {'success': False, 'message': 'Account not found or closed.'}
            
            acc.status = 'Inactive' if acc.status == 'Active' else 'Active'
            db.session.commit()
            return {'success': True, 'message': f'Account {acc.status.lower()}d.', 'data': acc.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}

    @staticmethod
    def close_account(account_id):
        try:
            acc = BankAccount.query.get(account_id)
            if not acc:
                return {'success': False, 'message': 'Account not found.'}
            
            acc.status = 'Closed'
            db.session.commit()
            return {'success': True, 'message': 'Account closed permanently.', 'data': acc.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': str(e)}
