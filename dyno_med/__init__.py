
from flask import Flask
from pymongo import MongoClient
from flask_wtf.csrf import CSRFProtect
from mongoengine import connect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dyno_med'
# database  connection using mongoclient
# This will be for registration
client = MongoClient('mongodb://127.0.0.1:27017')
school_collection = client.my_db.school

database = client.medical_system
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
csrf.exempt('dyno_med.routes.medical_practitioner_registration')

from dyno_med import routes
from dyno_med import medical_practitioners