from triage_app import db
from triage_app.models import User
from triage_app.users.forms import RegistrationForm, LoginForm
from flask import Blueprint, current_app, flash, url_for, render_template, request
from flask_login import (
    login_user, logout_user, current_user, login_required
)
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
            current_app.logger.info('User-{} ({} {}) logged in.'.format(user.id, user.firstname, user.lastname))
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login failed. Please check email and password', 'danger')
    else:
        flash('Login failed. Please check email and password', 'danger')
    return render_template('login.html', title='Log Into Surge Triage', form=form)
    
    return render_template('login.html')

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('register.html', title='Register for SIMS', form=form)
    else:
        if form.validate_on_submit():
            # check that slack id not already associated with an existing member
            existing_users_slack_ids = db.session.query(User).with_entities(User.slack_id).filter(User.slack_id != None).all()
            list_ids_to_check = []
            for id in existing_users_slack_ids:
                list_ids_to_check.append(id.slack_id)
            if form.slack_id.data in list_ids_to_check:
                flash('This Slack ID is already associated with a registered member.', 'danger')
                return render_template('register.html', title='Register for SIMS', form=form)
            
            # ping Slack API to get list of all members' ID, then compare form data to validate that user has entered valid ID
            try:
                slack_check = check_valid_slack_ids(form.slack_id.data)
            except:
                flash('Slack API is not responsive. Please contact a SIMS Portal administrator to complete registration.', 'danger')
                return render_template('register.html', title='Register for SIMS', form=form)
            if slack_check == False:
                flash('This Slack ID is not valid and does not belong to any existing SIMS Slack accounts.', 'danger')
                return render_template('register.html', title='Register for SIMS', form=form)
            else:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(firstname=form.firstname.data, lastname=form.lastname.data, ns_id=form.ns_id.data.ns_go_id, slack_id=form.slack_id.data, email=form.email.data, password=hashed_password)
                db.session.add(user)
                db.session.commit()
                message = "Thank you for registering for the SIMS Portal, {}. Your account has been placed into a queue, and will be approved by a SIMS Governance Committee member. You will be alerted here when that action is taken. In the meantime, you can log into the portal and explore the resources, but you will have limited permissions.".format(form.firstname.data)
                send_slack_dm(message, form.slack_id.data)
                new_user_slack_alert("A new user has registered on the SIMS Portal. Please review {}'s registration in the <{}/admin_landing|admin area>.".format(user.firstname, current_app.config['ROOT_URL']))
                flash('Your account has been created.', 'success')
                return redirect(url_for('users.login'))
        else:
            flash('Please correct the errors in the registration form.', 'danger')
        return render_template('register.html', title='Register for SIMS', form=form)