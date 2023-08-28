from triage_app import db
from triage_app.models import User
from flask import Blueprint, current_app, flash, url_for, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')