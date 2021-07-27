#!/usr/bin/env python

import os
from flask.config import Config
from app import create_app, db
from flask_script import Manager, Shell
# from app.models import User, Post, Tag, Category, Employee, Feedback
# from flask_migrate import MigrateCommand


app = create_app("test")
manager = Manager(app)


# def make_shell_context():
#     return dict(app=app, db=db, User=User, Post=Post, Tag=Tag,  Category=Category, Employee=Employee, Feedback=Feedback)

if __name__ == '__main__':
    manager.run()
