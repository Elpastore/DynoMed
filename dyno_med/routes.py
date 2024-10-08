#!/usr/bin/python3
from flask import jsonify, request, session, render_template, redirect, url_for, flash
from . import forms
from dyno_med.forms import RegistrationForm, LoginForm
import bcrypt
from flask_wtf.csrf import generate_csrf
# from dyno_med.Medical_pratitional import (med_forms, med_pract)
# from werkzeug.security import generate_password_hash
from .model.patient import *
from bson import ObjectId
#from bson.objectid import ObjectId
from flask_wtf.csrf import CSRFProtect
from dyno_med import (Medical, Expert, app, database, patient_record)
from datetime import datetime
from mongoengine import *

# csrf = CSRFProtect(app)
from dyno_med import csrf


# display home page
@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """The home page"""
    return render_template('home.html')

# get the calender page 
@app.route('/calender', methods=['GET'], strict_slashes=False)
def calender():
    """The home page"""
    return render_template('med-expert_calender_virtual.html')

# retrive and display learn more page
@app.route('/learn_more', methods=['GET'], strict_slashes=False)
def learn_more():
    """return the learnmore page"""
    return render_template('learn_more.html')

# not inised with this route yet
@app.route('/registration', methods=['POST'], strict_slashes=False)
def register_user():
    data = request.get_json()
    form = RegistrationForm(data=data, meta={'csrf': False})

    #data = request.json
    #form = RegistrationForm(data=data)
    
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
    """retirve the user credendials from the login form and save it in the database"""
    data = request.get_json()
    form = LoginForm(data=data, meta={'csrf': False})

    # check if all parameters are entered in the form
    if form.validate():
        email = form.email.data
        password = form.password.data.encode('utf-8')
        user = database.users.find_one({'email': email})
        
        # if user email and password exists in the database
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
    """get the user cache and logout"""
    # Logout logic to setup clearing cookies, tokens, or other authentication data
    # when a session will be setting up
    user_id = session.get('user_id')
    user = database.users.find_one({'_id': ObjectId(user_id)})
    if user_id:
        session.pop('user_id', None)
        return redirect(url_for('home'))
        # return jsonify({'message': f'{user["username"]} Logged out successfully'})
    else:
        return jsonify({'message': 'Not need to loggout since you are not login'})


@app.route('/user_signup-login', methods=['POST', 'GET'], strict_slashes=False)
@csrf.exempt
def login_signUp():
    """Login and signup for all users"""
    login_form = LoginForm()
    signup_form = RegistrationForm()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'form-signin':
            email = request.form.get('email')
            password = request.form.get('password')
            user_type = request.form.get('user_type')
            
            if login_form.validate_on_submit():
                expert = Expert.objects(email=email).first()
                user = database.users.find_one({'email': email, 'user_type': user_type})
                
                if user and user['user_type'] == 'patient':
                    if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                        session['user_id'] = str(user['_id'])
                        flash('Login success.', 'success')
                        return redirect(url_for('patient_profile'))
                    else:
                        flash('Login Unsuccessful. Please check your email and password.', 'danger')
                
                elif expert and bcrypt.checkpw(password.encode('utf-8'), expert.password.encode('utf-8')):
                    session['user_id'] = str(expert.id)
                    flash('Login success.', 'success')
                    return redirect(url_for('user_page'))
                else:
                    flash('Login Unsuccessful. Please check your email and password.', 'danger')

            return render_template('login.html', login_form=login_form, signup_form=signup_form)

        elif action == 'form-signup':
            if signup_form.validate_on_submit():
                username = signup_form.username.data
                email = signup_form.email.data
                password = signup_form.password.data
                user_type = request.form.get('user_type')

                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                try:
                    if user_type == 'patient':
                        new_user = {'username': username, 'email': email, 'password': hashed_password, 'user_type': user_type}
                        database.users.insert_one(new_user)
                        Patient(id=ObjectId(new_user['_id']), full_name=username, email=email).save()
                    elif user_type == 'medical':
                        expert = Expert(username=username, email=email, password=hashed_password)
                        expert.save()

                    flash('Registration successful. Please login.', 'success')
                    return redirect(url_for('login_signUp'))
                except Exception:
                    flash('Error in registration. Please try again!', 'danger')

            else:
                for field, errors in signup_form.errors.items():
                    for error in errors:
                        flash(f"Error in {getattr(signup_form, field).label.text}: {error}", 'danger')
                flash('Please try again!')
                
            return render_template('login.html', login_form=login_form, signup_form=signup_form)
    
    return render_template('login.html', login_form=login_form, signup_form=signup_form)

@app.route('/user_page', methods=['POST', 'GET'], strict_slashes=False)
@csrf.exempt
def user_page():
    """user page"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Unauthorized access'}), 401
    
    try:
        # retrive the expert object
        user = Expert.objects.get(id=user_id)
    except Exception as e:
        raise Exception("unable to retrive the user document: {e}")
    
    collection_name = user._get_collection_name()
    if collection_name == 'medical_practitioners':
        medical = Medical()
        med_dict = medical.retrieve_med_user(user)
    
    return render_template('user_page.html', med_user=med_dict, user=collection_name)


@app.route('/patient/profile', methods=['GET', 'POST', 'PUT'])
def patient_profile():
    user_id = session.get('user_id')
    # return render_template('patient_registration.html')
    # To be able to use this frontend part we will need the register and login frontend part
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
        
        #return jsonify(patient_user)
        
        return render_template('patient_profil.html', patient_data=patient_user)

@app.route('/user_page/account_setting', methods=['POST', 'GET'], strict_slashes=False)
@csrf.exempt
def account_setting():
    """Update account settings form"""
    from dyno_med import DoesNotExist, AccountSetting

    user_id = session.get('user_id')
    if not user_id:
        return AccountSetting.unauthorized_access()

    # Retrieve the user object from the database
    try:
        user = Expert.objects.get(id=user_id)
    except DoesNotExist:
        return AccountSetting.user_not_found()

    collection_name = user._get_collection_name()
    if collection_name == 'medical_practitioners':
        medical = Medical()
        med_user = medical.retrieve_med_user(user)

    if request.method == 'POST':
        data = request.json
        setting = AccountSetting()

        # change the email
        if 'email' in data:
            return setting.change_email(user, data)

        # change the account password
        elif 'new_password' in data:
            return setting.change_password(user, data)

        # change the account username of the user
        elif 'username' in data:
            return setting.change_username(user, data)

        # Deactivate account
        elif 'deactivate' in data:
            return setting.delete_account(user)

    return render_template('account_setting.html', med_user=med_user, user=collection_name)


@app.route('/account_setting/med_user_profile_setting', methods=['POST', 'GET'], strict_slashes=False)
@csrf.exempt
def med_user_profile_setting():
    """Update medical expert profile seetings form"""
    from dyno_med import DoesNotExist

    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'message': 'Unauthorized access'}), 401
    
    # Retrieve the medical user object from the database using the user_id
    try:
        # Retrieve the medical user object from the database using the user_id
        med_user = Expert.objects.get(id=user_id)
    except DoesNotExist:
        return jsonify({'message': 'Medical expert not found'}), 404
    

    if request.method == 'POST':
        form_name = request.form.get('form_name')
        medical = Medical()

        # ceck which form is submitted
        if form_name == 'education_form':
            education_data = request.form.to_dict(flat=False)

            # update the education form
            try:
                medical.update_med_user_education(med_user, education_data, None, user_id)
                return jsonify({'message': 'Education updated sucessfully'})
            except Exception as e:
                return jsonify({'message': str(e)}), 400
            
        elif form_name == 'address_form':
            address_data = request.form.to_dict()
            print('Adress Form Submitted:', address_data)
            # update the address form:
            try:
                medical.update_med_user_address(med_user, address_data, None, user_id)
                return jsonify({'message': 'Address update sucessfully'}), 200
            except Exception as e:
                return jsonify({'message': str(e)}), 400
        
        elif form_name == 'experirence_form':
            experience_data = request.form.to_dict()
            print('work experirnce form submitted:', experience_data)
            try:
                medical = Medical()
                medical.update_med_user_experience(med_user, experience_data, None, user_id)
                return jsonify({'meassage': 'work experience update sucessfully'}), 200
            except Exception as e:
                return jsonify({'message': str(e)}), 400
        
        elif form_name =='next_of_kin_form':
            next_of_kin_data = request.form.to_dict()
            print('work experirnce form submitted:', next_of_kin_data)
            try:
                medical = Medical()
                medical.update_med_user_kin(med_user, next_of_kin_data, None, user_id)
                return jsonify({'meassage': 'next_of_kin update sucessfully'}), 200
            except Exception as e:
                return jsonify({'meassage': str(e)}), 400
        
        elif form_name == 'profile_form':
            profile_data = request.form.to_dict()
            print('work experirnce form submitted:', profile_data)
            try:
                medical = Medical()
                medical.update_med_user_profile(med_user, profile_data, None, user_id)
                return jsonify({'meassage': 'profile update sucessfully'}), 200
            except Exception as e:
                return jsonify({'meassage': str(e)}), 400
        elif form_name == 'certification_form':
            certification_data = request.form.to_dict()
            cert_files= request.files.getlist('certificationFile[]')
            print('work experirnce form submitted:', certification_data)
            try:
                medical = Medical()
                medical.update_med_user_certifications(med_user, certification_data, cert_files, user_id)
                return jsonify({'meassage': 'certification update sucessfully'}), 200
            except Exception as e:
                return jsonify({'meassage': str(e)}), 400
        else:
            return jsonify({'message': 'Unknown form submitted'}), 400

    # If it's a GET request, render the template with the current user data
    return render_template('profile_setting.html', med_user=med_user)


@app.route('/patient_new_record', methods=['POST', 'GET'])
@csrf.exempt
def new_record():
    user_id = session.get('user_id')
    # user_id = '669bd069d5346b9bc0e962f3'
    """
    user_id = request.form(user_id)
    user = database.users.find_one({'id': user_id})
    """
    if not user_id:
        return jsonify({'message': 'Unauthorized access'}), 401
    
    if request.method == 'POST':
        try:
            # Extract basic patient information
            full_name = request.form.get('full_name')
            birthday = datetime.strptime(request.form.get('birthday'), '%Y-%m-%d')
            gender = request.form.get('gender')
            contact_information = request.form.get('contact_information')
            emergency_contact = request.form.get('emergency_contact')
            blood_group = request.form.get('blood_group')
            rhesus_factor = request.form.get('rhesus_factor')
            
            # Extract medical history data
            chief_complaint = request.form.get('chief_complaint')
            symptoms = request.form.get('symptoms').split(',') if request.form.get('symptoms') else []
            diagnoses = request.form.get('diagnoses').split(',') if request.form.get('diagnoses') else []
            by_doctor = request.form.get('by_doctor')
            blood_pressure = request.form.get('blood_pressure')
            heart_rate = int(request.form.get('heart_rate')) if request.form.get('heart_rate') else None
            temperature = float(request.form.get('temperature')) if request.form.get('temperature') else None
            respiration_rate = int(request.form.get('respiration_rate')) if request.form.get('respiration_rate') else None
            
            # Extract medications list
            medications = []
            index = 0
            while True:
                med_name = request.form.get(f'medications[{index}][name]')
                if not med_name:
                    break
                dosage = request.form.get(f'medications[{index}][dosage]')
                usage = request.form.get(f'medications[{index}][usage]')
                start_date = datetime.strptime(request.form.get(f'medications[{index}][start_date]'), '%Y-%m-%d')
                end_date = datetime.strptime(request.form.get(f'medications[{index}][end_date]'), '%Y-%m-%d')
                medications.append({
                    'name': med_name,
                    'dosage': dosage,
                    'usage': usage,
                    'start_date': start_date,
                    'end_date': end_date
                })
                index += 1
                
            appointments = []
            index = 0
            while True:
                appointment_date = request.form.get(f'appointments[{index}][date]')
                if not appointment_date:
                    break
                appointment_time = request.form.get(f'appointments[{index}][time]')
                doctor = request.form.get(f'appointments[{index}][doctor]')
                department = request.form.get(f'appointments[{index}][department]')
                appointments.append({
                    'date': datetime.strptime(appointment_date, '%Y-%m-%d'),
                    'time': appointment_time,
                    'doctor': doctor,
                    'department': department
                })
                index += 1

            # Extract immunization records
            immunization_records = request.form.get('immunization_records').split(',') if request.form.get('immunization_records') else []

            # Assuming you fetch user email from the database based on user_id
            email = database.users.find_one({'_id': ObjectId(user_id)})['email']

            # Create Patient object with associated MedicalRecord
            patient = Patient(
                id=user_id,
                full_name=full_name,
                birthday=birthday,
                gender=gender,
                contact_information=contact_information,
                emergency_contact=emergency_contact,
                email=email,
                blood_group=blood_group,
                rhesus_factor=rhesus_factor,
                medical_history=[
                    MedicalRecord(
                        chief_complaint=chief_complaint,
                        symptoms=symptoms,
                        diagnoses=diagnoses,
                        doctor=by_doctor,
                        vital_signs=VitalSigns(
                            blood_pressure=blood_pressure,
                            heart_rate=heart_rate,
                            temperature=temperature,
                            respiration_rate=respiration_rate
                        ),
                        medications=medications
                    )
                ],
                immunization_records=immunization_records,
                appointment= appointments
            )

            # Save patient to the database
            patient.save()

            return jsonify({'message': 'Patient profile updated successfully', 'patient_id': str(patient.id)})
        
        except Exception as e:
            return jsonify({'message': str(e)}), 400

    # If method is GET, return the patient registration form
    return render_template('patient_registration.html')


@app.route('/patient_update', methods=['POST', 'GET'])
@csrf.exempt
def update_record():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'message': 'Unauthorized access'}), 401

    if request.method == 'POST':
        data = request.form
        
        try:
            # Find the patient document by user_id
            patient_user = patient_record.patient.find_one({'_id': ObjectId(user_id)})
            if not patient_user:
                return jsonify({'message': 'Patient not found'}), 404
            
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
                'insurance_information': data.get('insurance_information', patient_user.get('insurance_information')),
                'medical_history': patient_user.get('medical_history')
            }

            medical_history = patient_user.get('medical_history', [])
            
            # Extract new medical history record from the form data
            chief_complaint = data.get('chief_complaint')
            symptoms = data.get('symptoms').split(',') if data.get('symptoms') else []
            diagnoses = data.get('diagnoses').split(',') if data.get('diagnoses') else []
            by_doctor = data.get('by_doctor')
            blood_pressure = data.get('blood_pressure')
            heart_rate = int(data.get('heart_rate')) if data.get('heart_rate') else None
            temperature = float(data.get('temperature')) if data.get('temperature') else None
            respiration_rate = int(data.get('respiration_rate')) if data.get('respiration_rate') else None
            
            # Extract medications list
            medications = []
            index = 0
            while True:
                med_name = data.get(f'medications[{index}][name]')
                if not med_name:
                    break
                dosage = data.get(f'medications[{index}][dosage]')
                usage = data.get(f'medications[{index}][usage]')
                start_date = datetime.strptime(data.get(f'medications[{index}][start_date]'), '%Y-%m-%d')
                end_date = datetime.strptime(data.get(f'medications[{index}][end_date]'), '%Y-%m-%d')
                medications.append({
                    'name': med_name,
                    'dosage': dosage,
                    'usage': usage,
                    'start_date': start_date,
                    'end_date': end_date
                })
                index += 1

            # Extract appointments list
            appointments = []
            index = 0
            while True:
                appointment_date = data.get(f'appointments[{index}][date]')
                if not appointment_date:
                    break
                appointment_time = data.get(f'appointments[{index}][time]')
                doctor = data.get(f'appointments[{index}][doctor]')
                department = data.get(f'appointments[{index}][department]')
                appointments.append({
                    'date': datetime.strptime(appointment_date, '%Y-%m-%d'),
                    'time': appointment_time,
                    'doctor': doctor,
                    'department': department
                })
                index += 1

            new_record = {
                'chief_complaint': chief_complaint,
                'symptoms': symptoms,
                'diagnoses': diagnoses,
                'doctor': by_doctor, 
                'vital_signs': {
                    'blood_pressure': blood_pressure, 
                    'heart_rate': heart_rate, 
                    'temperature': temperature, 
                    'respiration_rate': respiration_rate
                },
                'medications': medications,
                'appointments': appointments
            }

            update_data['medical_history'].append(new_record)

            patient_record.patient.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': update_data}
            )

            return jsonify({'message': 'Patient profile updated successfully'})
        except Exception as e:
            return jsonify({'message': f'An error occurred: {e}'}), 400

    # If method is GET, return the patient update form
    return render_template('patient_update.html')

def compute_age(birthdate):
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age
@app.route('/patient/profile/personal_info', methods=['GET', 'POST'], strict_slashes=False)
def personal_information():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Unauthorized access'}), 401
    
    try:
        # Convert the user_id to an ObjectId
        patient_user = patient_record.patient.find_one({'_id': ObjectId(user_id)})
    except Exception as e:
        return jsonify({'message': f'Invalid user ID: {e}'}), 400
    
    if not patient_user:
        return jsonify({'message': 'Patient not found'}), 404
    
    # Convert ObjectId to string for JSON serialization
    patient_user['_id'] = str(patient_user['_id'])
    month_names = {
    1: "Janvier",
    2: "Février",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Août",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décembre"
    }
    #return jsonify(patient_user)
    birthday = patient_user.get('birthday')

    if birthday:
        # Format the date into the desired string format
        formatted_date = f"{birthday.day} {month_names[birthday.month]} {birthday.year}"
        age = compute_age(birthday)
    else:
        formatted_date = "Unknow"
        age = 'Unknow'

    return render_template('patient_personal_info.html', patient_data=patient_user, birthday=formatted_date, age=age)   

@app.route('/patient/profile/appointment', methods=['GET', 'POST'], strict_slashes=False)
def patient_appointment():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Unauthorized access'}), 401
    
    try:
        # Convert the user_id to an ObjectId
        patient_user = patient_record.patient.find_one({'_id': ObjectId(user_id)})
    except Exception as e:
        return jsonify({'message': f'Invalid user ID: {e}'}), 400
    
    if not patient_user:
        return jsonify({'message': 'Patient not found'}), 404

    return render_template('patient_appointment.html', patient_data=patient_user)

@app.route('/patient/profile/medical_history', methods=['GET', 'POST'], strict_slashes=False)
def medical_history():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Unauthorized access'}), 401
    
    try:
        # Convert the user_id to an ObjectId
        patient_user = patient_record.patient.find_one({'_id': ObjectId(user_id)})
    except Exception as e:
        return jsonify({'message': f'Invalid user ID: {e}'}), 400
    
    if not patient_user:
        return jsonify({'message': 'Patient not found'}), 404

    return render_template('patient_medical_history.html', patient_data=patient_user)

@app.route('/patient/profile/medication', methods=['GET'], strict_slashes=False)
def patient_medication():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Unauthorized access'}), 401
    
    try:
        # Convert the user_id to an ObjectId
        patient_user = patient_record.patient.find_one({'_id': ObjectId(user_id)})
    except Exception as e:
        return jsonify({'message': f'Invalid user ID: {e}'}), 400
    
    if not patient_user:
        return jsonify({'message': 'Patient not found'}), 404

    return render_template('patient_medication.html', patient_data=patient_user)