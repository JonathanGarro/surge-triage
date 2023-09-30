import os
from flask import current_app
from twilio.rest import Client


def send_sms_twilio(body, from_num, to_num):
    account_sid = current_app.config['TWILIO_SID']
    auth_token = current_app.config['TWILIO_TOKEN']
    client = Client(account_sid, auth_token)
    
    message = client.messages \
        .create(
                body=body,
                from_=from_num,
                to=to_num
            )
    
    print(message.sid)
    return message.sid