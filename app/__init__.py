# import os
import rq
# import logging
# from logging.handlers import SMTPHandler, RotatingFileHandler
from redis import Redis
from flask import Flask
# from elasticsearch import Elasticsearch
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_cors import CORS
from config import config_dict


bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
login = LoginManager()
moment = Moment()
login.login_view = 'auth.login'
login.login_message = ('Please log in to access this page.')


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_dict[config_name])
    app.com
    bootstrap.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    CORS(app)

    # redis task queue
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('flask_proj-tasks', connection=app.redis)

    # not implemented yet!!!!
    # app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
    # if app.config['ELASTICSEARCH_URL'] else None

    # blueprint
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.calend import calend as calend_blueprint
    app.register_blueprint(calend_blueprint, url_prefix='/calendar')

    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.api import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.sale import sale as sale_bp
    app.register_blueprint(sale_bp, url_prefix='/sale')

    # send massage at email when app crushed
    # if not app.debug and not app.testing:
    #     if app.config['MAIL_SERVER']:
    #         auth = None
    #         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
    #             auth = (app.config['MAIL_USERNAME'],
    #                     app.config['MAIL_PASSWORD'])
    #         secure = None
    #         if app.config['MAIL_USE_TLS']:
    #             secure = ()
    #         mail_handler = SMTPHandler(
    #             mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
    #             fromaddr='no-reply@' + app.config['MAIL_SERVER'],
    #             toaddrs=app.config['ADMINS'], subject='Flask_proj Failure',
    #             credentials=auth, secure=secure)
    #         mail_handler.setLevel(logging.ERROR)
    #         app.logger.addHandler(mail_handler)

    #     if app.config['LOG_TO_STDOUT']:
    #         stream_handler = logging.StreamHandler()
    #         stream_handler.setLevel(logging.INFO)
    #         app.logger.addHandler(stream_handler)
    #     else:
    #         if not os.path.exists('logs'):
    #             os.mkdir('logs')
    #         file_handler = RotatingFileHandler('logs/flask_proj.log',
    #                                            maxBytes=10240, backupCount=10)
    #         file_handler.setFormatter(logging.Formatter(
    #             '%(asctime)s %(levelname)s: %(message)s '
    #             '[in %(pathname)s:%(lineno)d]'))
    #         file_handler.setLevel(logging.INFO)
    # #         app.logger.addHandler(file_handler)

    #     app.logger.setLevel(logging.INFO)
    #     app.logger.info('Microblog startup')

    return app
