
import pytest
from flask import current_app
from app import create_app



@pytest.fixture()
def app():
    app = create_app('testing')
    

    # other setup can go here

    yield app

    # clean up / reset resources here
@pytest.fixture()
def test_app_exists(self):
    assert(current_app is None)


def test_app_is_testing(self):
    assert(current_app.config['TESTING'])



@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()