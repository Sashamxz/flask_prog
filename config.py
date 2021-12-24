import os
import sys

basedir = os.path.abspath(os.path.dirname(__file__))



# # Platforma
# WIN = sys.platform.startswith('win')
# if WIN:
#     prefix = 'sqlite:///'
# else:
#     prefix = 'sqlite:////'

class Config():
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(' DEV_DATABASE_URL ')
    SECURITY_PASSWORD_SALT = os.environ.get('SALT')
    SECURITY_PASSWORD_HASH = 'bcrypt'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') 
    # or \
        # 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing'    : TestingConfig,
    'production': ProductionConfig}
