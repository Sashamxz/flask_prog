from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
# from flask_migrate import Migrate, MigrateCommand
# from flask_mail import Mail, Message
# from flask_script import Manager, Command, Shell
# from flask_login import LoginManager
from config import configs


bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(test):
    app = Flask(__name__)
    app.config.from_object(config['test'])
    configs['test'].init_app(app)
    bootstrap.init_app(app)
    # mail.init_app(app)
    # moment.init_app(app)
    db.init_app(app)
    # login_manager.init_app(app)
    # pagedown.init_app(app)
    return app

# mail = Mail(app)
# migrate = Migrate(app, db)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'


from . import views
