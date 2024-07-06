
from flask import Flask
from pymongo import MongoClient
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dyno_med'
client = MongoClient('mongodb://127.0.0.1:27017')
school_collection = client.my_db.school
database = client.dynoMed

# Initialize CSRF protection
csrf = CSRFProtect(app)
csrf.exempt('dyno_med.routes.register')

from dyno_med import routes
