from app.db import db
from datetime import datetime

class KYCSubmission(db.Model):
    __tablename__ = 'kyc_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    custom_id = db.Column(db.String(20), unique=True, nullable=False) 
    
    # Personal Info
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    
    # Documents
    aadhaar_number = db.Column(db.String(20), nullable=False)
    pan_number = db.Column(db.String(20), nullable=False)
    aadhaar_doc_path = db.Column(db.String(255), nullable=True)
    pan_doc_path = db.Column(db.String(255), nullable=True)
    
    # Status & Tracking (Pending, Verified, Rejected)
    status = db.Column(db.String(20), default="Pending") 
    reject_reason = db.Column(db.Text, nullable=True)
    submitted_on = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.custom_id,
            'name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'dob': self.dob,
            'address': self.address,
            'aadhaar': self.aadhaar_number,
            'pan': self.pan_number,
            'aadhaarDoc': self.aadhaar_doc_path,
            'panDoc': self.pan_doc_path,
            'status': self.status,
            'rejectReason': self.reject_reason,
            'submitted': self.submitted_on.strftime('%d %b %Y') if self.submitted_on else None
        }
