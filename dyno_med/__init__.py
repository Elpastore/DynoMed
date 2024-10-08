#!/usr/bin/env python3
""" module to initialize """
from flask import Flask
from pymongo import MongoClient
from flask_wtf.csrf import CSRFProtect
from mongoengine import connect

app = Flask(__name__)
print(f'Template folder: {app.template_folder}')

app.config['SECRET_KEY'] = 'dyno_med'

# connect using pymongodb
client = MongoClient('mongodb://127.0.0.1:27017')
database = client.dynoMed
patient_record = client.Record



# connection to the database using mongoengine
connect('dynoMed', host='mongodb://127.0.0.1:27017/dynoMed', alias='default')
record = connect('Record', alias="record", host='mongodb://127.0.0.1:27017/Record')


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

from .model.medExpertProfile_settings import Medical
# Import from med_expert.py in the model directory
from .model.med_expert import (Expert, Experience, NextOfKin, Certificate, Education,
                               ResidentialAddress)

# Import routes
from . import routes

# Import from med_pract.py in the model directory
from .model.medExpertAccount_settings import AccountSetting
from mongoengine import DoesNotExist

