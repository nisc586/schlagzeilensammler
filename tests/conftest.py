import pytest
from szsammler import create_app, db
from szsammler.config import TestConfig

@pytest.fixture()
def app():
    app = create_app(config_class=TestConfig)

    with app.app_context():
        # other setup can go here
        db.create_all()
        
        yield app

        # clean up / reset resources here
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()