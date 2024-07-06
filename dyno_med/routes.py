#!/usr/bin/python3
from flask import jsonify, request
from dyno_med import app, database
from dyno_med.forms import RegistrationForm
import bcrypt
from flask_wtf.csrf import generate_csrf

@app.route('/home', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to our Medical application system management'})

@app.route('/registration', methods=['POST'])
def register():
    data = request.get_json()
    form = RegistrationForm(data=data, meta={'csrf': False})
    
    if form.validate():
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        username = form.username.data
        email = form.email.data

        database['users'].insert_one({'username': username, 'email': email, 'password': hashed_password})
        return jsonify({'message': 'Your account has been successfully created! You are now able to log in'})
    
    errors = form.errors
    return jsonify({'message': 'Please try again, error occurred!', 'errors': errors})
