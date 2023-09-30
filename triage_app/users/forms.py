from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, FileField, SubmitField, BooleanField, IntegerField, DateField, DateTimeField, TextAreaField, SelectField, SelectMultipleField, RadioField
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from triage_app.models import User

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=40)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    slack_id = StringField('SIMS Slack ID', validators=[DataRequired()])
    phone_country = StringField('Cell Country Code', validators=[DataRequired(), Length(min=1, max=5)])
    phone = IntegerField('Cell Number (Integers Only)', validators=[DataRequired(), Length(min=1, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=24)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6, max=24), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered.')
            
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=24)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')