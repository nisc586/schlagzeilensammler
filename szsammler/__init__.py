from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from .config import Config

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(config_class=Config):
    print("⚡ Flask-App wird erstellt!") 

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        from .routes import main

        # TODO: What is best practice for creating the database? 
        db.create_all()
    
    app.register_blueprint(main)
    

    
    return app