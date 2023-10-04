from triage_app import db, bcrypt, mail
from triage_app.models import User
from triage_app.users.forms import RegistrationForm, LoginForm
from flask import Blueprint, current_app, flash, url_for, render_template, request, redirect
from flask_login import (
    login_user, logout_user, current_user, login_required
)
from flask_mail import Message, Mail
from flask_sqlalchemy import SQLAlchemy


users = Blueprint('users', __name__)

@users.route('/all_users')
def all_users():
    all_users = db.session.query(User).all()
    for user in all_users:
        print(user.first_name)
    return render_template('users_all.html', all_users=all_users)

@users.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'GET':
        return render_template('login.html', title='Log Into Surge Triage', form=form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            current_app.logger.info('User-{} ({} {}) logged in.'.format(user.id, user.first_name, user.last_name))
            flash('You have been logged in', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login failed. Please check email and password', 'danger')
    else:
        flash('Login failed. Please check email and password', 'danger')
    return render_template('login.html', title='Log Into Surge Triage', form=form)

@users.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('users.login_page'))

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'GET':
        return render_template('register.html', title='Register for SIMS', form=form)
    else:
        if request.method == 'POST' and form.validate_on_submit():
            # check if the email is already registered
            existing_user = db.session.query(User).filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email address is already registered. Please choose a different one.', 'danger')
                return redirect(url_for('users.register'))

            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data, 
                phone_country=form.phone_country.data, 
                phone=form.phone.data, 
                email=form.email.data, 
                password=hashed_password
            )
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created.', 'success')
            return redirect(url_for('users.login_page'))
        else:
            flash('Please correct the errors in the registration form.', 'danger')
        return render_template('register.html', title='Register for SIMS', form=form)
        
@users.route('/send_email/<int:user_id>', methods=['GET', 'POST'])
def send_email_verification(user_id):
    user_info = db.session.query(User).filter(User.id == user_id).first()
    user_name = user_info.first_name
    user_email = user_info.email
    
    msg = Message('Hello from the Surge Triage App!', sender=current_app.config['MAIL_USERNAME'], recipients=[user_email])
    msg.body = 'This is a test email sent from Flask-Mail.'
    mail.send(msg)
    flash('A verification email has been sent to {}.'.format(user_email), 'success')
    return redirect(url_for('users.login_page'))