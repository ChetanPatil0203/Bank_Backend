from app.models.user_model import UserRegister, UserLogin, PasswordReset
from app.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app.utils import generate_jwt_token
import random, string, smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app


class AuthService:

    # ─── REGISTER ─────────────────────────────────────────────────────────────
    @staticmethod
    def register_user(data):
        email = data.get('email')

        existing_user = UserLogin.query.filter_by(email=email).first()
        if existing_user:
            return {'success': False, 'message': 'Email already registered.'}

        password         = data.get('password')
        confirm_password = data.get('confirmPassword')

        if password != confirm_password:
            return {'success': False, 'message': 'Passwords do not match.'}

        hashed_password = generate_password_hash(password)

        try:
            dob_str = data.get('date_of_birth')
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None

            new_register = UserRegister(
                name=data.get('name'),
                email=email,
                mobile=data.get('mobile'),
                date_of_birth=dob,
                gender=data.get('gender')
            )
            new_login = UserLogin(
                email=email,
                password_hash=hashed_password
            )

            db.session.add(new_register)
            db.session.add(new_login)
            db.session.commit()

            return {'success': True, 'message': 'User registered successfully'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Server error: {str(e)}'}

    # ─── LOGIN ────────────────────────────────────────────────────────────────
    @staticmethod
    def login_user(data):
        email    = data.get('email')
        password = data.get('password')

        user_login = UserLogin.query.filter_by(email=email).first()

        if not user_login or not check_password_hash(user_login.password_hash, password):
            return {'success': False, 'message': 'Invalid Credentials!'}

        user_register = UserRegister.query.filter_by(email=email).first()

        try:
            token = generate_jwt_token(user_login.id, user_login.email)
            
            if not token:
                return {'success': False, 'message': 'Internal Error: Could not generate token.'}

            user_login.jwt_token = token
            db.session.commit()

            return {
                'success': True,
                'message': 'Login Successful! 🎉',
                'user':    user_register.to_dict() if user_register else {
                    'email': user_login.email, 'id': user_login.id
                },
                'token': token
            }
        except Exception as e:
            return {'success': False, 'message': f'Error generating token: {str(e)}'}

    # ─── FORGOT — STEP 1: Send OTP ────────────────────────────────────────────
    @staticmethod
    def forgot_send_otp(email: str):
        # Check user exists
        user = UserLogin.query.filter_by(email=email).first()
        if not user:
            return {'success': False, 'message': 'No account found with this email.'}

        # Generate 6-digit OTP
        otp    = "".join(random.choices(string.digits, k=6))
        expiry = datetime.utcnow() + timedelta(minutes=10)

        # Invalidate old OTPs
        PasswordReset.query.filter_by(email=email, is_used=False).update({'is_used': True})

        # Save new OTP
        reset = PasswordReset(email=email, otp=otp, otp_expiry=expiry)
        db.session.add(reset)
        db.session.commit()

        # Send email
        sent = AuthService._send_otp_email(email, otp)
        if not sent:
            return {'success': False, 'message': 'Failed to send OTP. Check email config in .env'}

        return {'success': True, 'message': 'OTP sent to your email address.'}

    # ─── FORGOT — STEP 2: Verify OTP ──────────────────────────────────────────
    @staticmethod
    def forgot_verify_otp(email: str, otp: str):
        reset = PasswordReset.query.filter_by(
            email=email, otp=otp, is_used=False
        ).filter(
            PasswordReset.otp_expiry > datetime.utcnow()
        ).order_by(PasswordReset.created_at.desc()).first()

        if not reset:
            return {'success': False, 'message': 'Invalid or expired OTP.'}

        # Mark OTP as used
        reset.is_used = True
        db.session.commit()

        return {'success': True, 'message': 'OTP verified successfully.'}

    # ─── FORGOT — STEP 3: Reset Password ──────────────────────────────────────
    @staticmethod
    def forgot_reset_password(email: str, new_password: str):
        user_login = UserLogin.query.filter_by(email=email).first()
        if not user_login:
            return {'success': False, 'message': 'User not found.'}

        user_login.password_hash = generate_password_hash(new_password)
        user_login.jwt_token     = None   # invalidate old tokens
        db.session.commit()

        return {'success': True, 'message': 'Password reset successfully! Please login.'}

    # ─── LOGOUT ────────────────────────────────────────────────────────────────
    @staticmethod
    def logout_user(token: str):
        try:
            user_login = UserLogin.query.filter_by(jwt_token=token).first()
            if not user_login:
                return {'success': False, 'message': 'Invalid token or already logged out.'}
                
            user_login.jwt_token = None
            db.session.commit()
            return {'success': True, 'message': 'Logged out successfully.'}
        except Exception as e:
            return {'success': False, 'message': f'Error logging out: {str(e)}'}

    # ─── EMAIL HELPER ─────────────────────────────────────────────────────────
    @staticmethod
    def _send_otp_email(to_email: str, otp: str) -> bool:
        sender_email    = os.getenv("GMAIL_USER", "")
        sender_password = os.getenv("GMAIL_PASSWORD", "")

        if not sender_email or not sender_password:
            print("[EMAIL] GMAIL_USER or GMAIL_PASSWORD not set in .env")
            return False

        html = f"""
        <div style="font-family:Arial,sans-serif;max-width:500px;margin:auto;
                    padding:32px;background:#f8faff;border-radius:16px;
                    border:1px solid #e2e8f0;">
          <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);
                      padding:24px;border-radius:12px;text-align:center;
                      margin-bottom:24px;">
            <h2 style="color:#fff;margin:0;">🔐 Password Reset</h2>
            <p style="color:rgba(255,255,255,0.6);margin:6px 0 0;font-size:13px;">
              OTP Verification
            </p>
          </div>
          <p style="color:#334155;font-size:15px;">Your One-Time Password is:</p>
          <div style="background:#fff;border:2px solid #e2e8f0;border-radius:12px;
                      padding:24px;text-align:center;margin:16px 0;">
            <span style="font-size:40px;font-weight:900;letter-spacing:14px;
                         color:#1a1a2e;font-family:monospace;">{otp}</span>
          </div>
          <p style="color:#64748b;font-size:13px;">
            ⏰ Expires in <strong>10 minutes</strong>.<br>
            🔒 Do not share this OTP with anyone.
          </p>
        </div>
        """

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Password Reset OTP"
            msg["From"]    = sender_email
            msg["To"]      = to_email
            msg.attach(MIMEText(html, "html"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, msg.as_string())

            print(f"[EMAIL] OTP sent to {to_email}")
            return True
        except Exception as e:
            print(f"[EMAIL ERROR] {e}")
            return False