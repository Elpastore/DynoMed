#!/usr/bin/python3
from flask import jsonify, request, session
from dyno_med import app, database
from dyno_med.forms import RegistrationForm, LoginForm
import bcrypt
from flask_wtf.csrf import generate_csrf
# from werkzeug.security import generate_password_hash

@app.route('/home', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to our Medical application system management'})

@app.route('/registration', methods=['POST'], strict_slashes=False)
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
    return jsonify({'message': 'Please try again, error occurred!', 'errors': errors}, 400)

@app.route('/login', methods=['POST'], strict_slashes=False)
def login():
    data = request.get_json()
    form = LoginForm(data=data, meta={'csrf': False})

    if form.validate():
        email = form.email.data
        password = form.password.data.encode('utf-8')
        user = database.users.find_one({'email': email})

        if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
            # setting up a session management
            return jsonify({'message': f'Welcome {user["username"]}, you are logged in'})
        else:
            return jsonify({'message': 'Login Unsuccessful. Please check your email and password.'}), 401

    errors = {field: error for field, error in form.errors.items()}
    return jsonify({'message': 'Please try again, errors occurred.', 'errors': errors}), 400

@app.route('/logout', methods=['GET'])
def logout():
    # Logout logic to setup clearing cookies, tokens, or other authentication data
    # when a session will be setting up
    return jsonify({'message': 'Logged out successfully'})