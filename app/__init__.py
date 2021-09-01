from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
# from flask_migrate import Migrate, MigrateCommand
# from flask_mail import Mail, Message
# from flask_script import Manager, Command, Shell
# from flask_login import LoginManager
import os
from config import DevelopmentConfig, configs
from flask_migrate import Migrate




bootstrap = Bootstrap()
db = SQLAlchemy()
# mail = Mail()
# login_manager = LoginManager()
# login_manager.login_view = 'login'
migrate = Migrate()

def create_app(config_name=None):
  

    app = Flask(__name__)
    app.config.from_object(configs['development'])
    configs['development'].init_app(app)
    bootstrap.init_app(app)

    # mail.init_app(app)
    # moment.init_app(app)
    with app.app_context():
        db.init_app(app)
    
    migrate.init_app(app, db)
    #blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .calend import calend as calend_blueprint
    app.register_blueprint(calend_blueprint, url_prefix='/calendar')

    return app







