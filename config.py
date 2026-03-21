import os
from dotenv import load_dotenv
from Settings.secret import Secret

load_dotenv()

class Config:
    ENV = os.getenv('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODICATIONS = True
    SECRET_KEY = Secret.get_secret_key()
    JWT_SECRET_KEY = Secret.get_jwt_secret_key()
    
    