import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv(override=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_dev_secret_key')
    
    # PostgreSQL Database configuration
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = urllib.parse.quote_plus(os.environ.get('DB_PASSWORD', ''))
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'payzen_bank')
    
    # Priority given to DATABASE_URL (Standard on Render)
    # Checking for multiple case variations to be robust
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or 
        os.environ.get('Database_URL') or 
        os.environ.get('database_url')
    )
    
    if SQLALCHEMY_DATABASE_URI:
        # SQLAlchemy 1.4+ requires 'postgresql://' instead of 'postgres://'
        if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    else:
        # Fallback to individual components
        # URL-encode the password to handle special characters safely
        DB_USER = os.environ.get('DB_USER', 'postgres')
        DB_PASSWORD = urllib.parse.quote_plus(os.environ.get('DB_PASSWORD', ''))
        DB_HOST = os.environ.get('DB_HOST', 'localhost')
        DB_PORT = os.environ.get('DB_PORT', '5432')
        DB_NAME = os.environ.get('DB_NAME', 'payzen_bank')
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Configuration
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    # MAX_CONTENT_LENGTH removed to allow unlimited upload sizes
    # Google Gemini API Configuration
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')
