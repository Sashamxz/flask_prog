#!/usr/bin/env python

import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


from app import create_app, db
from flask_migrate import Migrate, upgrade
from app.models import Post
# from flask_migrate import MigrateCommand



app = create_app(config_name='testing')
manager = Migrate(app,db)


# def make_shell_context():
#     return dict(app=app, db=db, User=User, Post=Post, Tag=Tag,  Category=Category, Employee=Employee, Feedback=Feedback)

if __name__ == '__main__':
    manager.run()
