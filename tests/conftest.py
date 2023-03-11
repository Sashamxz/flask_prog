import pytest
from app import create_app
from flask_sqlalchemy import SQLAlchemy


@pytest.fixture(scope='module')
def app():
    app = create_app('testing')
    with app.app_context():
        db = SQLAlchemy(app=app)
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope='function')
def db(app):
    with app.app_context():
        db = SQLAlchemy(app=app)
        db.create_all()
        yield db
        db.session.remove()


@pytest.fixture(scope='function')
def client(app, db):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='function')
def runner(app, db):
    with app.test_cli_runner() as runner:
        yield runner
