#!/usr/bin/python3
from flask import jsonify, request, session
from dyno_med import app, database, patient_record
from dyno_med.forms import RegistrationForm, LoginForm
import bcrypt
from flask_wtf.csrf import generate_csrf
from dyno_med.dyno_med.Medical_pratitional import (med_forms, med_pract)
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
        user_type = form.user_type.data

        database['users'].insert_one({'username': username, 'email': email, 'password': hashed_password, 'user_type': user_type})
        return jsonify({'message': f'Your account has been successfully created! You are now able to log in as a {user_type}'})
    
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
    user_id = session.get('user_id')
    user = database.users.find_one({'_id': ObjectId(user_id)})
    if user_id:
        session.pop('user_id', None)
        return jsonify({'message': f'{user["username"]} Logged out successfully'})
    else:
        return jsonify({'message': 'Not need to loggout since you are not login'})


@app.route('/medical_practitioner/registration', methods=['POST'])
def medical_practitioner_registration():
    med_data = request.get_json()
    form = med_forms.MedicalPersonel(data=med_data, meta={'csrf': False})
    
    if request.method == 'POST':
        if form.validate_on_submit():
            return med_pract.Medical.insert_db(form)
        
        errors = form.errors
        return jsonify({'message': 'Registration failed due to validation errors.', 'errors': errors}, 400)

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
        
        return jsonify(patient_user)
    
    elif request.method == 'POST':
        data = request.get_json()
        user = database.users.find_one({'_id': ObjectId(user_id)})
        if user:
            if user.user_type == 'patient':
                return jsonify({'message': 'You don"t have access to this part!'}), 401
            # Create patient data using user's _id as the _id field in MongoDB
            patient = Patient(
            # id = ObjectId(user.id),  # not working
            full_name=data['full_name'],
            birthday=datetime.strptime(data['birthday'], '%Y-%m-%d'),
            gender=data['gender'],
            blood_group = data['blood_group'],
            rhesus_factor = data['rhesus_factor'],
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
    elif request.method == 'PUT':
        data = request.get_json()
        try:
            # Find the patient document by user_id
            patient_user = patient_record.patient.find_one({'_id': ObjectId(user_id)})
            if not patient_user:
                return jsonify({'message': 'Patient not found'}), 404
            if user.user_type == 'patient':
                return jsonify({'message': 'You don"t have access to this part!'}), 401
            
            # Update patient data with provided data
            update_data = {
                'full_name': data.get('full_name', patient_user.get('full_name')),
                'birthday': datetime.strptime(data['birthday'], '%Y-%m-%d') if 'birthday' in data else patient_user.get('birthday'),
                'gender': data.get('gender', patient_user.get('gender')),
                'contact_information': data.get('contact_information', patient_user.get('contact_information')),
                'emergency_contact': data.get('emergency_contact', patient_user.get('emergency_contact')),
                'blood_group': data.get('blood_group', patient_user.get('blood_group')),
                'rhesus_factor': data.get('rhesus_factor', patient_user.get('rhesus_factor')),
                'immunization_records': data.get('immunization_records', patient_user.get('immunization_records')),
                'insurance_information': data.get('insurance_information', patient_user.get('insurance_information'))
            }
            
            if 'medical_history' in data:
                update_data['medical_history'] = [
                    {
                        'chief_complaint': mh['chief_complaint'],
                        'symptoms': mh['symptoms'],
                        'diagnoses': mh['diagnoses'],
                        'surgeries': [
                            {
                                'procedure': surgery['procedure'],
                                'date': datetime.strptime(surgery['date'], '%Y-%m-%d'),
                                'outcome': surgery['outcome']
                            } for surgery in mh['surgeries']
                        ],
                        'allergies': [
                            {
                                'name': allergy['name'],
                                'reaction': allergy['reaction']
                            } for allergy in mh['allergies']
                        ],
                        'vital_signs': {
                            'blood_pressure': mh['vital_signs']['blood_pressure'],
                            'heart_rate': mh['vital_signs']['heart_rate'],
                            'temperature': mh['vital_signs']['temperature'],
                            'respiration_rate': mh['vital_signs']['respiration_rate']
                        },
                        'medications': [
                            {
                                'name': med['name'],
                                'dosage': med['dosage'],
                                'start_date': datetime.strptime(med['start_date'], '%Y-%m-%d'),
                                'end_date': datetime.strptime(med['end_date'], '%Y-%m-%d')
                            } for med in mh['medications']
                        ]
                    } for mh in data['medical_history']
                ]
            
            # Update the patient document
            patient_record.patient.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': update_data}
            )

            return jsonify({'message': 'Patient profile updated successfully'})
        except Exception as e:
            return jsonify({'message': f'An error occurred: {e}'}), 400

    else:
        return jsonify({'message': 'Method not allowed'}), 405
