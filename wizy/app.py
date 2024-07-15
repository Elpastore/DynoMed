#!/usr/bin/python3
"""
Main route of the application
"""
from flask import (Flask, request, render_template, url_for, redirect, flash)
from model.med_pract import Medical
from  model import database
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = 'dyno_med'

@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """The home page"""
    return render_template('home.html')

@app.route('/user_signup-login', methods=['POST', 'GET'], strict_slashes=False)
@csrf.exempt
def login_signUp():
    """signup or login as a user"""
    if request.method == 'POST':
        action = request.form['action']
        if action == "signin":
            email = request.form['email']
            password = request.form['password']
            print(f"email:{email}, password:{password}")
            med = Medical()
            response = med.login(email, password)
            if response == None:
                flash('you are not a registered user! please signUp')
            print(response)
            return render_template('med-expert_profile.html', response=response)
        if action == 'signup':
            form_data = request.form
            med = Medical()
            med.insert(form_data)
    return render_template('login.html')
    

@app.route('/medical_practitioner/profile', methods=['POST', 'GET'], strict_slashes=False)
@csrf.exempt
def medical_expert_page():
    """medical expert page"""
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('med-expert_profile.html')

@app.route('/medical_practitioner/registration', methods=['POST', 'GET'], strict_slashes= False)
@csrf.exempt
def medical_practitioner_registration():
    """register medical experts"""
    if request.method == 'POST':
        form_data = request.form
        print("Received form data:", form_data)
        med = Medical()
        med.insert(form_data)
        return redirect(url_for('home'))

    return render_template('med-expert_reg.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)