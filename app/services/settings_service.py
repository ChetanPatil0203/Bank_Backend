from app.models.user_model import UserRegister, UserLogin, UserPreference, LoginAudit
from app.models.account_model import AccountRequest, BankAccount
from app.db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class SettingsService:

    @staticmethod
    def get_profile(user_id):
        try:
            user_login = UserLogin.query.get(user_id)
            if not user_login:
                return {'success': False, 'message': 'User not found.'}

            email = user_login.email
            register_user = UserRegister.query.filter_by(email=email).first()
            if not register_user:
                return {'success': False, 'message': 'Profile data not found.'}

            profile_data = register_user.to_dict()
            
            # Fetch latest AccountRequest to get address and KYC status/account info
            account_request = AccountRequest.query.filter_by(email=email).order_by(AccountRequest.created_at.desc()).first()
            
            if account_request:
                # Fallback address if not set in register
                if not profile_data.get('address') or profile_data['address'] == "—":
                    profile_data['address'] = account_request.address

            profile_data['account'] = None
            
            if account_request and account_request.status == 'Approved':
                # Fetch bank account linked to this request
                bank_account = BankAccount.query.filter_by(request_id=account_request.id).first()
                if bank_account:
                    acc_dict = bank_account.to_dict()
                    acc_dict['father_name'] = account_request.father_name
                    acc_dict['nominee_name'] = account_request.nominee_name
                    acc_dict['nominee_relation'] = account_request.nominee_relation
                    acc_dict['aadhaar'] = account_request.aadhaar
                    acc_dict['pan'] = account_request.pan
                    
                    profile_data['account'] = acc_dict

            return {'success': True, 'data': profile_data}
        except Exception as e:
            return {'success': False, 'message': f'Error fetching profile: {str(e)}'}

    @staticmethod
    def update_profile(user_id, data):
        try:
            user_login = UserLogin.query.get(user_id)
            if not user_login:
                return {'success': False, 'message': 'User not found.'}

            register_user = UserRegister.query.filter_by(email=user_login.email).first()
            if not register_user:
                return {'success': False, 'message': 'Profile data not found.'}

            if 'name' in data:
                register_user.name = data['name']
            if 'mobile' in data:
                register_user.mobile = data['mobile']
            if 'address' in data:
                register_user.address = data['address']
            if 'dob' in data:
                try:
                    register_user.date_of_birth = datetime.strptime(data['dob'], '%Y-%m-%d').date()
                except:
                    pass
            if 'gender' in data:
                register_user.gender = data['gender']

            db.session.commit()
            return {'success': True, 'message': 'Profile updated successfully!', 'data': register_user.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Error updating profile: {str(e)}'}

    @staticmethod
    def get_preferences(user_id):
        try:
            pref = UserPreference.query.filter_by(user_id=user_id).first()
            if not pref:
                pref = UserPreference(user_id=user_id)
                db.session.add(pref)
                db.session.commit()
            
            return {'success': True, 'data': pref.to_dict()}
        except Exception as e:
            return {'success': False, 'message': f'Error fetching preferences: {str(e)}'}

    @staticmethod
    def update_preferences(user_id, data):
        try:
            pref = UserPreference.query.filter_by(user_id=user_id).first()
            if not pref:
                pref = UserPreference(user_id=user_id)
                db.session.add(pref)

            if 'email' in data:
                pref.email_notifications = data['email']
            if 'sms' in data:
                pref.sms_notifications = data['sms']
            if 'push' in data:
                pref.push_notifications = data['push']
            if 'security' in data:
                pref.security_alerts = data['security']
            if 'transactions' in data:
                pref.transaction_alerts = data['transactions']
            if 'offers' in data:
                pref.offer_promotions = data['offers']

            db.session.commit()
            return {'success': True, 'message': 'Preferences updated!', 'data': pref.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Error updating preferences: {str(e)}'}

    @staticmethod
    def change_password(user_id, data):
        try:
            current_pwd = data.get('oldPassword') # frontend calls it oldPassword
            new_pwd = data.get('newPassword')

            user = UserLogin.query.get(user_id)
            if not user or not check_password_hash(user.password_hash, current_pwd):
                return {'success': False, 'message': 'Current password incorrect.'}

            user.password_hash = generate_password_hash(new_pwd)
            user.jwt_token = None
            db.session.commit()

            return {'success': True, 'message': 'Password changed successfully! Please login again.'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Error changing password: {str(e)}'}

    @staticmethod
    def get_login_activity(user_id):
        try:
            user = UserLogin.query.get(user_id)
            if not user:
                return {'success': False, 'message': 'User not found.'}
            
            audits = LoginAudit.query.filter_by(email=user.email).order_by(LoginAudit.created_at.desc()).limit(10).all()
            
            activity = []
            for a in audits:
                activity.append({
                    'id': a.id,
                    'status': a.status,
                    'ip': a.ip_address,
                    'time': a.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return {'success': True, 'data': activity}
        except Exception as e:
            return {'success': False, 'message': f'Error fetching activity: {str(e)}'}
