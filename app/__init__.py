from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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
db = SQLAlchemy(app)

# mail = Mail(app)
# migrate = Migrate(app, db)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'





if __name__=='__main__':
    app.run(host='localhost',debug=True)
