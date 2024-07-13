#!/usr/bin/python3
"""
Main route of the application
"""
from flask import (Flask, request, render_template, url_for, redirect)
from model import med_pract
from  model import database
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = 'dyno_med'

@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """The home page"""
    return render_template('home.html')

@app.route('/medical_practitioner/registration', methods=['POST', 'GET'], strict_slashes= False)
def medical_practitioner_registration():
    """register medical experts"""
    if request.method == 'POST':
        med_data = request.get_json()
        data = med_pract.Medical.insert_db(med_data)
        print(data)
        return redirect(url_for('registration Successful'))
    
    practitioners = list(database.medical_practitioner.find())        
    return render_template('med-expert_reg.html', practitioners=practitioners)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
