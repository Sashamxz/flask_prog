from importlib.resources import path
import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.join(os.path.dirname(__file__))




class Config():
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')
    FLASK_ADMIN = os.getenv('FLASK_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SECURITY_PASSWORD_SALT = os.getenv('SALT')
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig}
