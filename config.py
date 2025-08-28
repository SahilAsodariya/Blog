import os
from dotenv import load_dotenv
import stripe

load_dotenv()

class Config:
    DB_USER = os.getenv("DB_USER", "flaskuser")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "mypassword")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "myflaskdb")
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
   
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt')
    DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1", "yes"]
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    # Gmail SMTP configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))  # Must be integer
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1', 'yes']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_TEST')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY_TEST')
    WTF_CSRF_ENABLED = False


