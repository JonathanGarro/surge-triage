from flask import Flask
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from triage_app.config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from triage_app.main.routes import main
    
    app.register_blueprint(main)
    
    with app.app_context():
        from triage_app import models
        db.create_all()
    
    return app