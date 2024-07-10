#!/usr/bin/python3
from flask import jsonify, request, session
from dyno_med import app, database, patient_record
from dyno_med.forms import RegistrationForm, LoginForm
import bcrypt
from flask_wtf.csrf import generate_csrf
from Medical_pratitional.Doctor import MedicalPersonel
# from werkzeug.security import generate_password_hash
from model.patient import *
from bson import ObjectId
#from bson.objectid import ObjectId

@app.route('/home', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to our Medical application system management'})

@app.route('/registration', methods=['POST'], strict_slashes=False)
def register_user():
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
            user_id = str(user['_id'])
            session['user_id'] = user_id
            
            return jsonify({'message': f'Welcome {user["username"]}, you are logged in', 'Id': user_id})
        else:
            return jsonify({'message': 'Login Unsuccessful. Please check your email and password.'}), 401

    errors = {field: error for field, error in form.errors.items()}
    return jsonify({'message': 'Please try again, errors occurred.', 'errors': errors}), 400

@app.route('/logout', methods=['GET'])
def logout():
    # Logout logic to setup clearing cookies, tokens, or other authentication data
    # when a session will be setting up
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'})

@app.route('/patient/registration', methods=['POST'])
def patient_registration():
    data = request.get_json()
    form = RegistrationForm(data=data, meta={'csrf': False})
    
    if form.validate():
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        username = form.username.data
        email = form.email.data

        new_user = database['users'].insert_one({'username': username, 'email': email, 'password': hashed_password})
        return jsonify({'message': f'Your account has been successfully created! You are now able to log in with id: {new_user.inserted_id}'})
    
    errors = form.errors
    return jsonify({'message': 'Please try again, error occurred!', 'errors': errors}, 400)

@app.route('/patient/profile', methods=['GET', 'POST'])
def patient_profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Unauthorized access'}), 401

    if request.method == 'GET':            
        try:
            # Convert the user_id to an ObjectId
            patient_user = patient_record.patient.find_one({'_id': ObjectId(user_id)})
        except Exception as e:
            return jsonify({'message': f'Invalid user ID: {e}'}), 400
        
        if not patient_user:
            return jsonify({'message': 'Patient not found'}), 404
        
        # Convert ObjectId to string for JSON serialization
        patient_user['_id'] = str(patient_user['_id'])
        
        return jsonify(patient_user['full_name'])
    
    elif request.method == 'POST':
        data = request.get_json()
        user = database.users.find_one({ '_id': user_id })
        if user:
            # Create patient data using user's _id as the _id field in MongoDB
            patient = Patient(
            id = ObjectId(user.id),  # not working
            full_name=data['full_name'],
            birthday=datetime.strptime(data['birthday'], '%Y-%m-%d'),
            gender=data['gender'],
            medical_history=[MedicalRecord(
                    chief_complaint=data['medical_history']['chief_complaint'],
                    symptoms=data['medical_history']['symptoms'],
                    diagnoses=data['medical_history']['diagnoses'],
                    surgeries=data['medical_history']['surgeries'],
                    allergies=data['medical_history']['allergies'],
                    
                    vital_signs=VitalSigns(
                        blood_pressure=data['medical_history']['vital_signs']['blood_pressure'],
                        heart_rate=data['medical_history']['vital_signs']['heart_rate'],
                        temperature=data['medical_history']['vital_signs']['temperature'],
                        respiration_rate=data['medical_history']['vital_signs']['respiration_rate']),
                    
                    medications=[
                        Medication(
                            name=med['name'],
                            dosage=med['dosage'],
                            start_date=datetime.strptime(med['start_date'], '%Y-%m-%d'),
                            end_date=datetime.strptime(med['end_date'], '%Y-%m-%d')
                        ) for med in data['medical_history']['medications']
                    ]
                )],
            immunization_records=data['immunization_records']
            )
            
            patient.save()

            return jsonify({'message': 'Patient profile created successfully', 'patient_id': str(patient.id)})
        else:
            return jsonify({'message': 'Patient not found in the users database'})

    else:
        return jsonify({'message': 'Method not allowed'}), 405

        
    # return the html file with patient option
@app.route('/reg_medical_personel', methods=['PSOT', 'GET'], strict_slashes=False)
def reg_medical_personel():
    """register all medical personel"""
    form = MedicalPersonel()
    
