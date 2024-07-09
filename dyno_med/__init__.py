
from flask import Flask
from pymongo import MongoClient
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dyno_med'
client = MongoClient('mongodb://127.0.0.1:27017')
school_collection = client.my_db.school

# Added by wizy
medical_practitioners = client.dynoMed.medical_practitioners

database = client.dynoMed

# Added by wizy


# Initialize CSRF protection
csrf = CSRFProtect(app)
csrf.exempt('dyno_med.routes.register')
csrf.exempt('dyno_med.routes.login')

from dyno_med import routes
from dyno_med import medical_practitioners