#!/usr/bin/env python3
""" module to initialize """
from flask import Flask
from pymongo import MongoClient
from flask_wtf.csrf import CSRFProtect
from mongoengine import connect

app = Flask(__name__)
print(f'Template folder: {app.template_folder}')

app.config['SECRET_KEY'] = 'dyno_med'
# database  connection using mongoclient
# This will be for registration

# connect using pymongodb
client = MongoClient('mongodb://127.0.0.1:27017')

# database = client.medical_system
database = client.dynoMed
patient_record = client.Record

# Added by wizy
medical_practitioners = client.dynoMed.medical_practitioners


# connection to the database using mongoengine
record = connect('Record', host='mongodb://127.0.0.1:27017/Record')


# Initialize CSRF protection
csrf = CSRFProtect(app)

# Exempt specific routes from CSRF protection
'''csrf._exempt_views.add('dyno_med.routes.register_patient')
csrf._exempt_views.add('dyno_med.routes.login')'''
csrf.exempt('dyno_med.routes.register')
csrf.exempt('dyno_med.routes.login')
csrf.exempt('dyno_med.routes.patient_registration')
csrf.exempt('dyno_med.routes.patient_profile')
csrf.exempt('dyno_med.routes.add_new_medical_record')

# csrf.exempt('dyno_med.routes.medical_practitioner_registration')

from dyno_med import routes
#from dyno_med import medical_pract
