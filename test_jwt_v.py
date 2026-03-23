import sys
import os
from flask import Flask

# Add project root to sys.path
sys.path.append(os.getcwd())

from app.utils import generate_jwt_token, decode_jwt_token

def test_jwt():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test_secret'
    
    with app.app_context():
        # Test Generation
        user_id = 123
        email = "test@example.com"
        token = generate_jwt_token(user_id, email)
        
        if not token:
            print("❌ Token generation failed!")
            return
        
        print(f"✅ Token generated: {token[:20]}...")
        
        # Test Decoding
        decoded = decode_jwt_token(token)
        if not decoded:
            print("❌ Token decoding failed!")
            return
        
        if decoded.get('user_id') == user_id and decoded.get('email') == email:
            print("✅ Token decoding successful: data matches!")
        else:
            print(f"❌ Token decoding data mismatch: {decoded}")

if __name__ == "__main__":
    test_jwt()
