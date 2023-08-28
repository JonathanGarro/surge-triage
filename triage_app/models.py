from triage_app import db, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from flask_login import UserMixin, current_user
from sqlalchemy import Column, ForeignKey, Integer, Table

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    slack_id = db.Column(db.String)