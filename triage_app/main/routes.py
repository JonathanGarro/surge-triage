import logging
from triage_app import db, bcrypt
from triage_app.models import User
from triage_app.sms.utils import send_sms_twilio

from flask import (
    Blueprint, current_app, flash, url_for, render_template, redirect, request
)

from flask_login import login_required



main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')
    
@main.route('/test_sms')
def test_sms():
    body = "Testing surge triage alert"
    from_num = "+18447524809"
    to_num = "+17073392253"
    
    send_sms_twilio(body, from_num, to_num)
    
    return redirect(url_for('main.index'))
    
@main.route('/send_notification/<int:country_code>/<int:phone_number>/<int:emergency_id>/<int:role_id>', methods=['GET', 'POST'])
@login_required
def send_notification(country_code, phone_number, emergency_id, role_id):
    role_type = db.session.query(Roles).filter(Roles.id == role_id).first()
    body = "A new information management surge alert in response to {} has been released which may fit your profile. A {} has been requested to support the operation. Please respond with 1 if you are interested and available for deployment soon, or 0 if you are not."
    