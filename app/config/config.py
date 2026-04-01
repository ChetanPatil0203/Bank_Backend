import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_dev_secret_key')
    
    # MySQL Database configuration
    DB_USER = os.environ.get('DB_USER', 'root')
    # URL-encode the password to handle special characters like '@' safely
    DB_PASSWORD = urllib.parse.quote_plus(os.environ.get('DB_PASSWORD', ''))
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'payzen_bank')
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Configuration
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    # MAX_CONTENT_LENGTH removed to allow unlimited upload sizes
    # Google Gemini API Configuration
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')
