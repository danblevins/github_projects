from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import requests
import random
import pandas as pd
account_sid = os.environ.get('twilio_sid')
auth_token = os.environ.get('twilio_token')

app=Flask(__name__)
Bootstrap(app)

### Web pages ###
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/sms/", methods=['GET', 'POST'])
def sms_reply():
    data = pd.read_csv("TheOfficeSMS.csv")
    data['Character'] = data['Character'].str.lower()
    resp=MessagingResponse()
    body=request.values.get("Body",None).lower().strip().replace(" ","")

    data = data[data['Character'] == str(body)].reset_index(drop=True)
    randint=random.randint(0, len(data['Character']))
    resp.message(data['Line'][randint])
    return str(resp)

if __name__ == '__main__':
    app.run(debug=False)