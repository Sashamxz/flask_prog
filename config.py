import os
from pickle import FALSE
from dotenv import load_dotenv




load_dotenv()
basedir = os.path.join(os.path.dirname(__file__))




class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')
    FLASK_ADMIN = os.getenv('FLASK_ADMIN')
    WTF_CSRF_ENABLED = False
    SECURITY_PASSWORD_SALT = os.getenv('SALT')
    SECURITY_PASSWORD_HASH = 'bcrypt'
    FLASKY_COMMENTS_PER_PAGE  = 5
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USE_TLS = 1
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    ADMINS = ['zontick99@gmail.com']
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER') 
    REDIS_URL = os.getenv('REDIS_URL') or 'redis://'
    
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SUPPRESS_SEND = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL') or \
        'sqlite://'
    WTF_CSRF_ENABLED = False



class ProductionConfig(Config):
    pass


class DockerConfig(Config):
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DOCKER_DATABASE_URL')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
    
   


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,}
