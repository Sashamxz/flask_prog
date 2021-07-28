from flask import Flask

from flask_bootstrap import Bootstrap
# from flask_migrate import Migrate, MigrateCommand
# from flask_mail import Mail, Message
# from flask_script import Manager, Command, Shell
# from flask_login import LoginManager
import os, config
from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)
bootstrap = Bootstrap(app)


# mail = Mail(app)
# migrate = Migrate(app, db)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'


from . import views
