import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'payzen_bank')

def verify_admin():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Check if AdminLogin table exists
        cursor.execute("SELECT email FROM admin_login WHERE email = 'Payzen2026@gmail.com'")
        admin = cursor.fetchone()

        if admin:
            print(f"SUCCESS: Admin found: {admin[0]}")
        else:
            print("FAILURE: Admin not found.")

        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_admin()
