from app.db import db
from datetime import datetime

class AccountRequest(db.Model):
    __tablename__ = 'account_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    bank_holder_name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text, nullable=False)
    aadhaar = db.Column(db.String(12), unique=True, nullable=False)
    pan = db.Column(db.String(10), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    nominee_name = db.Column(db.String(100), nullable=False)
    nominee_relation = db.Column(db.String(100), nullable=False)
    signature_name = db.Column(db.String(100), nullable=True)
    reason = db.Column(db.Text, nullable=True)
    
    # File paths for uploaded documents
    photo_path = db.Column(db.String(255), nullable=True)
    aadhaar_path = db.Column(db.String(255), nullable=True)
    pan_path = db.Column(db.String(255), nullable=True)
    
    status = db.Column(db.String(20), default='Pending') # Pending, Approved, Rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'bank_holder_name': self.bank_holder_name,
            'father_name': self.father_name,
            'dob': self.dob.strftime('%Y-%m-%d') if self.dob else None,
            'gender': self.gender,
            'mobile': self.mobile,
            'email': self.email,
            'address': self.address,
            'aadhaar': self.aadhaar,
            'pan': self.pan,
            'account_type': self.account_type,
            'branch': self.branch,
            'nominee_name': self.nominee_name,
            'nominee_relation': self.nominee_relation,
            'signature_name': self.signature_name,
            'reason': self.reason,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'photo_url': f"/api/v1/admin/uploads/{self.photo_path}" if self.photo_path else None,
            'aadhaar_url': f"/api/v1/admin/uploads/{self.aadhaar_path}" if self.aadhaar_path else None,
            'pan_url': f"/api/v1/admin/uploads/{self.pan_path}" if self.pan_path else None,
            'docs': {
                'photo': bool(self.photo_path),
                'aadhaar': bool(self.aadhaar_path),
                'pan': bool(self.pan_path)
            }
        }

class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    ifsc = db.Column(db.String(20), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    bank_holder_name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=True)
    balance = db.Column(db.Numeric(15, 2), default=0.00)
    status = db.Column(db.String(20), default='Active') # Active, Inactive, Closed
    opened_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Link to the original request
    request_id = db.Column(db.Integer, db.ForeignKey('account_requests.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'account_number': self.account_number,
            'ifsc': self.ifsc,
            'account_type': self.account_type,
            'type': self.account_type,     # Frontend-friendly alias
            'bank_holder_name': self.bank_holder_name,
            'branch': self.branch or "—",
            'balance': float(self.balance),
            'status': self.status,
            'opened_at': self.opened_at.isoformat() if self.opened_at else None
        }
