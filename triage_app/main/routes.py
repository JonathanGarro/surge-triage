import logging
from triage_app import db, bcrypt
from triage_app.alerts.utils import get_latest_surge_alerts, extract_text, format_date
from triage_app.models import User, Alert
from triage_app.sms.utils import send_sms_twilio

from flask import (
    Blueprint, current_app, flash, url_for, render_template, redirect, request
)

from flask_login import login_required
from sqlalchemy import desc


main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/dashboard')
@login_required
def dashboard():
    surge_alerts = db.session.query(Alert).order_by(desc(Alert.alert_id)).all()
    for alert in surge_alerts:
        # preprocessing of text for table
        alert.molnix_created_at = alert.molnix_created_at[:10]
        alert.message = extract_text(alert.message) # regex to remove rotation and other unneeded data from 'message'
        alert.event_id = alert.event_id[3:] # strip out 'OP-'
        alert.closes = format_date(alert.closes)
        alert.start = format_date(alert.start)
        alert.end = format_date(alert.end)
    
    return render_template('dashboard.html', surge_alerts=surge_alerts)

@main.route('/test_sms')
def test_sms():
    body = "Testing surge triage alert"
    from_num = "+18447524809"
    to_num = "+17073392253"
    
    send_sms_twilio(body, from_num, to_num)
    
    return redirect(url_for('main.index'))

@main.route('/test')
def run_test():
    get_latest_surge_alerts()
    return redirect(url_for('main.dashboard'))

@main.route('/send_notification/<int:country_code>/<int:phone_number>/<int:emergency_id>/<int:role_id>', methods=['GET', 'POST'])
@login_required
def send_notification(country_code, phone_number, emergency_id, role_id):
    role_type = db.session.query(Roles).filter(Roles.id == role_id).first()
    body = "A new information management surge alert in response to {} has been released which may fit your profile. A {} has been requested to support the operation. Please respond with 1 if you are interested and available for deployment soon, or 0 if you are not."
    