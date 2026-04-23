from app.db import db
from datetime import datetime

class UserRegister(db.Model):
    __tablename__ = 'register'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d') if self.date_of_birth else None,
            'gender': self.gender,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UserLogin(db.Model):
    __tablename__ = 'login'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    jwt_token = db.Column(db.Text, nullable=True)
    failed_attempts = db.Column(db.Integer, default=0)
    lockout_until   = db.Column(db.DateTime, nullable=True)
    last_login_at   = db.Column(db.DateTime, nullable=True)


class LoginAudit(db.Model):
    __tablename__ = 'login_audits'
    
    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(120), nullable=False)
    status     = db.Column(db.String(100), nullable=False) # 'Success', 'Failed', 'Lockout'
    ip_address = db.Column(db.String(45), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AdminLogin(db.Model):
    __tablename__ = 'admin_login'
    
    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    jwt_token       = db.Column(db.Text, nullable=True)
    login_time      = db.Column(db.DateTime, nullable=True)
    failed_attempts = db.Column(db.Integer, default=0)
    lockout_until   = db.Column(db.DateTime, nullable=True)


# ✅ NEW — Password Reset OTP table (auto-created by SQLAlchemy)
class PasswordReset(db.Model):
    __tablename__ = 'password_resets'

    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(120), nullable=False, index=True)
    otp        = db.Column(db.String(10), nullable=False)
    otp_expiry = db.Column(db.DateTime, nullable=False)
    is_used    = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ✅ NEW — User Preferences table for notification settings
class UserPreference(db.Model):
    __tablename__ = 'user_preferences'

    id                 = db.Column(db.Integer, primary_key=True)
    user_id            = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=False, unique=True)
    email_notifications = db.Column(db.Boolean, default=True)
    sms_notifications   = db.Column(db.Boolean, default=True)
    push_notifications  = db.Column(db.Boolean, default=False)
    security_alerts     = db.Column(db.Boolean, default=True)
    transaction_alerts  = db.Column(db.Boolean, default=True)
    offer_promotions    = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'email': self.email_notifications,
            'sms': self.sms_notifications,
            'push': self.push_notifications,
            'security': self.security_alerts,
            'transactions': self.transaction_alerts,
            'offers': self.offer_promotions
        }
