#!/usr/bin/env python

import sys
from flask_script import Manager
from flask_migrate import Migrate
from app import create_app, db
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)


# @app.cli.command()
# def deploy():
#     """Run deployment tasks."""
#     # migrate database to latest revision
#     upgrade()


if __name__ == '__main__':

    app.run(host="10.0.0.66", port='7777', debug=True)
