from triage_app import db, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from flask_login import UserMixin, current_user
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, relationship, column_property

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone = db.Column(db.Integer) # enforce with regex to remove dashes and other punctuation
    phone_country = db.Column(db.String) # string because some country codes use dash
    email = db.Column(db.String)
    slack_id = db.Column(db.String)
    password = db.Column(db.String(120), nullable=False)
    
    triages = db.relationship('Triage', backref='triaged_member')
    
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())
    
    fullname = column_property(first_name + " " + last_name)

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
    
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())
    
class Triage(db.Model):
    __tablename__ = "triages"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    alert_id = db.Column(db.Integer, db.ForeignKey('alerts.id'))
    user_response = db.Column(db.Integer, db.ForeignKey('responses.id'))
    user_comments = db.Column(db.String)
    
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())
    
class Response(db.Model):
    __tablename__ = "responses"
    
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String)
    
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())
    