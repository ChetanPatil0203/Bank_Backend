import os
import smtplib
from dotenv import load_dotenv

load_dotenv(override=True)

sender_email = os.getenv("GMAIL_USER")
sender_password = os.getenv("GMAIL_PASSWORD")

print(f"Testing with Email: {sender_email}")
print(f"Password length: {len(sender_password) if sender_password else 0}")

# Test 1: SMTP 587 with STARTTLS
print("\n--- Testing Port 587 with STARTTLS ---")
try:
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
        print("Connected to smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        print("STARTTLS completed")
        server.ehlo()
        server.login(sender_email, sender_password)
        print("Login SUCCESSFUL!")
except Exception as e:
    print(f"FAILED: {e}")

# Test 2: SMTP_SSL 465
print("\n--- Testing Port 465 with SSL ---")
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
        print("Connected to smtp.gmail.com:465 (SSL)")
        server.login(sender_email, sender_password)
        print("Login SUCCESSFUL!")
except Exception as e:
    print(f"FAILED: {e}")
