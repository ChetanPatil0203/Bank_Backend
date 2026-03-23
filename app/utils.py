import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_jwt_token(user_id, email):
    """
    Generates a JWT token for a user.
    """
    try:
        payload = {
            'user_id': user_id,
            'email':   email,
            'exp':     datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    except Exception as e:
        print(f"[JWT ERROR] Error generating token: {e}")
        return None

def decode_jwt_token(token):
    """
    Decodes a JWT token using the app's secret key.
    """
    try:
        return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        print("[JWT ERROR] Token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("[JWT ERROR] Invalid token.")
        return None
    except Exception as e:
        print(f"[JWT ERROR] Error decoding token: {e}")
        return None
