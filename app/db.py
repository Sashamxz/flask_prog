from flask_sqlalchemy import SQLAlchemy
from app import app
from config import Configuration



def init_db(app):
    db = SQLAlchemy(app)
    return db