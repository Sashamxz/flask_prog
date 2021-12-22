from flask import Flask
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os
from config import DevelopmentConfig, configs
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore


bootstrap = Bootstrap()
db = SQLAlchemy()
# mail = Mail()
# login_manager = LoginManager()
# login_manager.login_view = 'login'
migrate = Migrate()

from app.models import Post, Role, Tag, User 

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

def create_app(config_name=None):
  
    app = Flask(__name__)
    app.config.from_object(configs['development'])
    configs['development'].init_app(app)
    bootstrap.init_app(app)
    
    # mail.init_app(app)
    # moment.init_app(app)
    
    db.init_app(app)
       
    admin = Admin(app)
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Tag, db.session))
    admin.init_app
    migrate.init_app(app, db)
    #blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .calend import calend as calend_blueprint
    app.register_blueprint(calend_blueprint, url_prefix='/calendar')
    #user_create
    security = Security(app, user_datastore)

    return app






# admin.add_view(ModelView(User, db.session))
#  admin.add_view(ModelView(Post, db.session))
