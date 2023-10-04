from triage_app import db
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from triage_app.models import Alert
import requests
import json
import math
import csv
import re
from datetime import datetime

def extract_text(input_string):
    """
    The message column from the GO API sometimes isn't properly formatted. This utility removes the text that comes after a comma or after the rotation number.
    """
    # search for comma, 2nd or 3rd
    pattern = r',|2nd|3rd'
    
    # split the input string based on the pattern
    parts = re.split(pattern, input_string)
    
    return parts[0]
    
def format_date(date_str):
    if date_str:
        original_date = datetime.strptime(date_str[:10], '%Y-%m-%d')
        formatted_date = original_date.strftime('%b %d, %Y')
        return formatted_date
    else:
        return ""

def get_latest_surge_alerts():
    api_call = 'https://goadmin.ifrc.org/api/v2/surge_alert/'
    r = requests.get(api_call).json()
    
    # get existing alerts from the local db
    existing_alerts = db.session.query(Alert).order_by(Alert.alert_id.desc()).all()
    # create list of ids
    existing_alert_ids = [alert.alert_id for alert in existing_alerts]

    # page flipper for paginated surge alerts
    current_page = 1
    #page_count = int(math.ceil(r['count'] / 50))
    page_count = 1
    
    count_new_records = 0
    
    output = []
    
    while current_page <= page_count:
        for result in r['results']:
            temp_dict = {}
            temp_dict['alert_id'] = result['id']
            temp_dict['message'] = result['message']
            temp_dict['molnix_id'] = result['molnix_id']
            temp_dict['created_at'] = result['created_at']
            temp_dict['opens'] = result['opens']
            temp_dict['closes'] = result['closes']
            temp_dict['start'] = result['start']
            temp_dict['end'] = result['end']
            
            for tag in result['molnix_tags']:
                groups = tag['groups']
                
                if 'LANGUAGE' in groups:
                    temp_dict['language'] = tag['description']
                if 'rotation' in groups:
                    temp_dict['rotation'] = tag['description']
                if 'ALERT TYPE' in groups:
                    temp_dict['scope'] = tag['description']
                if 'Modality' in groups:
                    temp_dict['modality'] = tag['description']
                if 'REGION' in groups:
                    temp_dict['region'] = tag['description']
                if 'OPERATIONS' in groups:
                    temp_dict['event_name'] = tag['description']
                    temp_dict['event_id'] = tag['name']
                if 'ROLES' in groups:
                    # roles has two values nested inside
                    try:
                        next_index = groups.index('ROLES') + 1
                        temp_dict['sector'] = groups[next_index]
                    except IndexError:
                        temp_dict['sector'] = 'Missing Sector' 
            
            if temp_dict.get('alert_id') is not None:
                output.append(temp_dict)
                
            if r['next']:
                next_page = requests.get(r['next']).json()
                r = next_page
                current_page += 1
            else:
                break
    
    # check for alerts not already in db and save
    for alert in output:
        if alert and alert['alert_id'] not in existing_alert_ids:
            try:
                individual_alert = Alert(
                    alert_id = alert['alert_id'],
                    message = alert['message'],
                    molnix_id = alert['molnix_id'],
                    molnix_created_at = alert['created_at'],
                    opens = alert['opens'],
                    closes = alert['closes'],
                    start = alert['start'],
                    end = alert['end'],
                    region = alert['region'],
                    language = alert['language'],
                    sector = alert['sector'],
                    modality = alert['modality'],
                    scope = alert['scope'],
                    rotation = alert['rotation'],
                    event_name = alert['event_name'],
                    event_id = alert['event_id']
                )
            except Exception as e:
                current_app.logger.error("error saving alert object via get_latest_surge_alerts function: {}".format(e))
            try:
                db.session.add(individual_alert)
                db.session.commit()
                count_new_records += 1
            except:
                pass
    
    date = datetime.today()
    current_app.logger.info("get_latest_surge_alerts ran: {}".format(date))