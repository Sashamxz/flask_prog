#!/usr/bin/env python

import os
from flask_migrate import Migrate
from flask_script import Manager
from app import create_app, db
from dotenv import load_dotenv
from app.models import User,  Role, Permission, Post, Comment, Like



dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)


@app.shell_context_processor
def make_shell_context():
    return {db: db, User: User, Post: Post, Comment: Comment,
     Like: Like, Role:Role, Permission:Permission,}





if __name__ == '__main__':
    
    app.run(host="0.0.0.0", port='5000')
