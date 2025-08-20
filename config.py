import os
from dotenv import load_dotenv
import stripe

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
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
