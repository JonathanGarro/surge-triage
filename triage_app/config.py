import os

class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TWILIO_SID = os.environ.get('TWILIO_SID')
    TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')