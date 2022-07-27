import pytest
from app import create_app
from app.models import db


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.init_app(app)
        db.create_all()
            
  

    return app



@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

