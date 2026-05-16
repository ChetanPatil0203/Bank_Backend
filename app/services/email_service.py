import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    @staticmethod
    def send_account_approval_email(to_email, name, account_number, ifsc):
        sender_email = os.environ.get('GMAIL_USER')
        sender_password = os.environ.get('GMAIL_PASSWORD')
        
        if not sender_email or not sender_password:
            print(">>> ERROR: Email credentials not found in environment variables. <<<")
            return False

        subject = "Welcome to Payzen Bank - Account Approved!"
        body = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
                <h2 style="color: #2b6cb0;">Congratulations, {name}!</h2>
                <p>Your account request has been successfully <strong>Approved</strong> by Payzen Bank.</p>
                <div style="background-color: #f7fafc; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 5px 0;"><strong>Account Number:</strong> {account_number}</p>
                    <p style="margin: 5px 0;"><strong>IFSC Code:</strong> {ifsc}</p>
                </div>
                <p>You can now log in to the Payzen Bank application using your registered mobile number and start banking with us.</p>
                <p>Thank you for choosing Payzen Bank.</p>
                <p style="color: #666; font-size: 12px; margin-top: 30px;">This is an automated message. Please do not reply.</p>
            </div>
        </body>
        </html>
        """

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"Payzen Bank <{sender_email}>"
        message["To"] = to_email

        html_part = MIMEText(body, "html")
        message.attach(html_part)

        try:
            # Using context manager for safe connection handling
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, message.as_string())
            print(f">>> Email sent successfully to {to_email} <<<")
            return True
        except Exception as e:
            print(f">>> ERROR sending email: {e} <<<")
            return False
    @staticmethod
    def send_transaction_alert_email(to_email, name, txn_type, amount, balance, timestamp, note):
        sender_email = os.environ.get('GMAIL_USER')
        sender_password = os.environ.get('GMAIL_PASSWORD')
        
        if not sender_email or not sender_password:
            return False

        subject = f"Transaction Alert: {txn_type} of ₹{amount}"
        color = "#e53e3e" if txn_type in ['Withdraw', 'Transfer Out'] else "#38a169"
        
        body = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
                <h2 style="color: {color};">Transaction Alert</h2>
                <p>Hello {name},</p>
                <p>This is to inform you of a recent transaction on your Payzen Bank account.</p>
                
                <div style="background-color: #f7fafc; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 5px 0;"><strong>Type:</strong> {txn_type}</p>
                    <p style="margin: 5px 0;"><strong>Amount:</strong> ₹{amount}</p>
                    <p style="margin: 5px 0;"><strong>Current Balance:</strong> ₹{balance}</p>
                    <p style="margin: 5px 0;"><strong>Date:</strong> {timestamp}</p>
                    {f'<p style="margin: 5px 0;"><strong>Note:</strong> {note}</p>' if note else ''}
                </div>
                
                <p>If you did not authorize this transaction, please contact us immediately.</p>
                <p>Thank you for banking with Payzen.</p>
                <p style="color: #666; font-size: 12px; margin-top: 30px;">This is an automated security alert.</p>
            </div>
        </body>
        </html>
        """

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"Payzen Bank Security <{sender_email}>"
        message["To"] = to_email

        html_part = MIMEText(body, "html")
        message.attach(html_part)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, message.as_string())
            print(f">>> Transaction Email sent successfully to {to_email} <<<")
            return True
        except Exception as e:
            print(f">>> ERROR sending transaction email: {e} <<<")
            return False
    @staticmethod
    def send_otp_email(to_email, otp, context="Verification"):
        sender_email = os.environ.get('GMAIL_USER')
        sender_password = os.environ.get('GMAIL_PASSWORD')
        
        if not sender_email or not sender_password:
            return False

        subject = f"{context} OTP - Payzen Bank"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f7f6; padding: 20px;">
            <div style="max-width: 500px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid #e0e0e0;">
                <div style="text-align: center; margin-bottom: 25px;">
                    <h2 style="color: #1e3a8a; margin: 0;">🔐 {context}</h2>
                </div>
                <p style="color: #4b5563; font-size: 16px; line-height: 1.5;">Hello,</p>
                <p style="color: #4b5563; font-size: 16px; line-height: 1.5;">Your One-Time Password (OTP) for <strong>{context}</strong> is:</p>
                <div style="background-color: #f3f4f6; padding: 20px; border-radius: 10px; text-align: center; margin: 25px 0;">
                    <span style="font-size: 36px; font-weight: 900; letter-spacing: 8px; color: #1e3a8a;">{otp}</span>
                </div>
                <p style="color: #6b7280; font-size: 14px; line-height: 1.5; text-align: center;">
                    This OTP is valid for 10 minutes. Please do not share this code with anyone.
                </p>
                <hr style="border: 0; border-top: 1px solid #e5e7eb; margin: 25px 0;">
                <p style="color: #9ca3af; font-size: 12px; text-align: center;">
                    This is an automated security message from Payzen Bank.
                </p>
            </div>
        </body>
        </html>
        """

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"Payzen Security <{sender_email}>"
        message["To"] = to_email

        html_part = MIMEText(body, "html")
        message.attach(html_part)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, message.as_string())
            return True
        except Exception as e:
            print(f">>> ERROR sending OTP email: {e} <<<")
            return False
