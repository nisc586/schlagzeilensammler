from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from .config import Config

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_class=Config):
    print("⚡ Flask-App wird erstellt!") 

    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .routes import main  # delayed import to avoid circular import
        # TODO: What is best practice for creating the database? 
        db.create_all()

    
    app.register_blueprint(main)
        
    return app