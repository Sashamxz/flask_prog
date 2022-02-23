from flask import Flask, current_app
from flask import redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
# from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from flask_admin import Admin
from flask_mail import Mail
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import current_user
from config import  config






bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
# moment = Moment()
babel = Babel()
# login_manager = LoginManager()
# login_manager.login_view = 'login'



from app.models import Post, Role, Tag, User 


user_datastore = SQLAlchemyUserDatastore(db, User, Role)


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name,  **kwargs):
        return redirect( url_for('security.login', next =request.url))  


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass         


class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title',  'body', 'tags' ]


class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['name']



def create_app(config_name=None): 
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    # moment.init_app(app)
    babel.init_app(app)


    db.init_app(app)
       
    admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
    admin.add_view(PostAdminView(Post, db.session))
    admin.add_view(TagAdminView(Tag, db.session))
    
    #blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .calend import calend as calend_blueprint
    app.register_blueprint(calend_blueprint, url_prefix='/calendar')
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    #user_create
    security = Security(app, user_datastore)

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])




# admin.add_view(ModelView(User, db.session))
#  admin.add_view(ModelView(Post, db.session))
