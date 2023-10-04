from flask import Flask
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from triage_app.config import Config
import os

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' 
login_manager.login_message_category = 'danger'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    mail.init_app(app)
    
    from triage_app.main.routes import main
    from triage_app.users.routes import users
    
    app.register_blueprint(main)
    app.register_blueprint(users)
    
    return app