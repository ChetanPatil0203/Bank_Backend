import os
import random, string, smtplib
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from app.db import db
from app.models.kyc_model import KYCSubmission
from app.models.user_model import PasswordReset
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class KycService:
    # ─── SEND OTP ─────────────────────────────────────────────────────────────
    @staticmethod
    def send_kyc_otp(email: str):
        email = email.strip().lower()

        # Generate 6-digit OTP
        otp = "".join(random.choices(string.digits, k=6))
        expiry = datetime.utcnow() + timedelta(minutes=10)

        # Invalidate old OTPs
        PasswordReset.query.filter_by(email=email, is_used=False).update({'is_used': True})

        # Save new OTP
        reset = PasswordReset(email=email, otp=otp, otp_expiry=expiry)
        db.session.add(reset)
        db.session.commit()

        # Send email
        sent = KycService._send_otp_email(email, otp)
        if not sent:
            return {'success': False, 'message': 'Failed to send OTP. Check email config in .env'}

        return {'success': True, 'message': 'OTP sent to your email address for verification.'}

    # ─── VERIFY OTP ───────────────────────────────────────────────────────────
    @staticmethod
    def verify_kyc_otp(email: str, otp: str):
        email = email.strip().lower()
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

    # ─── SUBMIT KYC ───────────────────────────────────────────────────────────
    @staticmethod
    def submit_kyc(data, files, upload_folder):
        email = data.get('email', '').strip().lower()
        
        # We assume UI hit verify_otp before this or backend checks it here.
        # But UI flows differ. Let's just store the KYC request now.
        
        existing_kyc = KYCSubmission.query.filter_by(email=email).first()
        if existing_kyc and existing_kyc.status in ['Pending', 'Verified']:
            return {'success': False, 'message': f'A KYC request for this email is already {existing_kyc.status}.'}

        try:
            # Handle Files
            aadhaar_filename = None
            pan_filename = None
            
            if 'aadhaarFile' in files:
                a_file = files['aadhaarFile']
                if a_file.filename != '':
                    extension = a_file.filename.rsplit('.', 1)[1].lower() if '.' in a_file.filename else 'pdf'
                    aadhaar_filename = f"aadhaar_{datetime.now().strftime('%Y%m%d%H%M%S')}.{extension}"
                    a_file.save(os.path.join(upload_folder, aadhaar_filename))

            if 'panFile' in files:
                p_file = files['panFile']
                if p_file.filename != '':
                    extension = p_file.filename.rsplit('.', 1)[1].lower() if '.' in p_file.filename else 'pdf'
                    pan_filename = f"pan_{datetime.now().strftime('%Y%m%d%H%M%S')}.{extension}"
                    p_file.save(os.path.join(upload_folder, pan_filename))

            # Generate Custom ID (KYC + Count + 1)
            count = KYCSubmission.query.count()
            custom_id = f"KYC{(count + 1):03d}"  # KYC001, KYC002...

            new_kyc = KYCSubmission(
                custom_id=custom_id,
                full_name=data.get('fullName'),
                email=email,
                phone=data.get('mobile'),
                dob=data.get('dob'),
                address=data.get('address'),
                aadhaar_number=data.get('aadhaar'),
                pan_number=data.get('pan'),
                aadhaar_doc_path=aadhaar_filename or data.get('aadhaar_doc_path'), # fallback for testing
                pan_doc_path=pan_filename or data.get('pan_doc_path'),             # fallback for testing
                status="Pending"
            )

            db.session.add(new_kyc)
            db.session.commit()

            return {
                'success': True, 
                'message': 'KYC Submitted successfully! Currently under review.',
                'data': new_kyc.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Failed to submit KYC: {str(e)}'}

    # ─── GET ALL KYCs (ADMIN) ─────────────────────────────────────────────────
    @staticmethod
    def get_all_kycs():
        try:
            kycs = KYCSubmission.query.order_by(KYCSubmission.submitted_on.desc()).all()
            return {'success': True, 'data': [k.to_dict() for k in kycs]}
        except Exception as e:
            return {'success': False, 'message': f'Error fetching KYCs: {str(e)}'}

    # ─── UPDATE KYC STATUS (ADMIN) ────────────────────────────────────────────
    @staticmethod
    def update_kyc_status(custom_id: str, new_status: str, reject_reason: str = None):
        if new_status not in ["Verified", "Rejected", "Pending"]:
            return {'success': False, 'message': 'Invalid status provided.'}

        kyc = KYCSubmission.query.filter_by(custom_id=custom_id).first()
        if not kyc:
            return {'success': False, 'message': 'KYC submission not found.'}

        kyc.status = new_status
        if new_status == "Rejected":
            if not reject_reason:
                return {'success': False, 'message': 'Reject reason is required.'}
            kyc.reject_reason = reject_reason
        else:
            kyc.reject_reason = None

        try:
            db.session.commit()
            return {'success': True, 'message': f'KYC successfully {new_status}.'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'Error updating status: {str(e)}'}

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
          <div style="background:linear-gradient(135deg,#0f1f4b,#153e75);
                      padding:24px;border-radius:12px;text-align:center;
                      margin-bottom:24px;">
            <h2 style="color:#fff;margin:0;">🪪 KYC Verification</h2>
            <p style="color:rgba(255,255,255,0.7);margin:6px 0 0;font-size:13px;">
              Email OTP Verification
            </p>
          </div>
          <p style="color:#334155;font-size:15px;">Your One-Time Password to submit KYC is:</p>
          <div style="background:#fff;border:2px solid #e2e8f0;border-radius:12px;
                      padding:24px;text-align:center;margin:16px 0;">
            <span style="font-size:40px;font-weight:900;letter-spacing:14px;
                         color:#0f1f4b;font-family:monospace;">{otp}</span>
          </div>
          <p style="color:#64748b;font-size:13px;">
            ⏰ Expires in <strong>10 minutes</strong>.<br>
            🔒 Please do not share this OTP with anyone.
          </p>
        </div>
        """

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "KYC Verification OTP"
            msg["From"]    = sender_email
            msg["To"]      = to_email
            msg.attach(MIMEText(html, "html"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, msg.as_string())

            return True
        except Exception as e:
            print(f"[EMAIL ERROR] {e}")
            return False
