from flask import Flask
from pymongo import MongoClient
from flask_wtf.csrf import CSRFProtect
from mongoengine import connect

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dyno_med'

# Database connection using MongoClient
client = MongoClient('mongodb://127.0.0.1:27017')
database = client.dynoMed

# Connection to the database using mongoengine
record = connect('Record', host='mongodb://127.0.0.1:27017/Record')

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Exempt specific routes from CSRF protection
csrf.exempt('medical_practitioner_registration')
