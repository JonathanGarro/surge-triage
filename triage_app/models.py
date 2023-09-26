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

class Alert(db.Model):
    __tablename__ = "alerts"
    
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.Integer)
    message = db.Column(db.String)
    molnix_id = db.Column(db.Integer)
    molnix_created_at = db.Column(db.String)
    opens = db.Column(db.String)
    closes = db.Column(db.String)
    start = db.Column(db.String)
    end = db.Column(db.String)
    region = db.Column(db.String)
    language = db.Column(db.String)
    sector = db.Column(db.String)
    modality = db.Column(db.String)
    scope = db.Column(db.String)
    rotation = db.Column(db.String)
    event_name = db.Column(db.String)
    event_id = db.Column(db.String)