#!/usr/bin/env python

import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


from app import create_app, db
from flask_migrate import Migrate, upgrade





app = create_app('development')



# def make_shell_context():
#     return dict(app=app, db=db, Post=Post)





if __name__ == '__main__':
    app.run()
