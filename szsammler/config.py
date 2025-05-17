import os

class Config:
    # TODO: SECRET_KEY??
    SECRET_KEY = os.getenv("SECRET_KEY", "default")
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


# Different environments can inherit from Config
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SECRET_KEY = "test"