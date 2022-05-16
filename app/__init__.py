import logging
from flask import Flask, request, current_app
from flask import redirect, url_for, request
from elasticsearch import Elasticsearch
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import config




bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ('Please log in to access this page.')











def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    db.init_app(app)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    # blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .calend import calend as calend_blueprint
    app.register_blueprint(calend_blueprint, url_prefix='/calendar')

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # from app.api import bp as api_bp
    # app.register_blueprint(api_bp, url_prefix='/api')

    # user_create
    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask_proj startup')
    
   
    

    return app


from app import models