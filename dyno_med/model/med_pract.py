#!/usr/bin/env python
"""module for all medical practitioners"""
from dyno_med import medical_practitioners
from datetime import datetime
from werkzeug.utils import secure_filename
import os

from mongoengine import  Document, EmbeddedDocument, StringField, ListField, EmbeddedDocumentField, DateTimeField, IntField, FloatField, DateField
from datetime import datetime
from mongoengine import connect


class Medical:
    def __init__(self):
        """Initialize the Medical class"""
        self.collection = medical_practitioners
        self.UPLOAD_FOLDER = '/home/pc/DynoMed/dyno_med/file_DataBase'  # Set this to your desired upload path
        self.ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
    
    def create_user(self, email, hashed_password, username):
        """find the user associated with the given email"""
        new_practitioner = {
        'username': username,
        'email': email,
        'passWord': hashed_password,
        'first_name': None,
        'middle_name': None,
        'last_name': None,
        'age': None,
        'gender': None,
        'date_of_birth': None,
        'country_of_origin': None,
        'state_of_origin': None,
        'local_government_area': None,
        'town_of_origin': None,
        'mobile_num': None,
        'linkedin': None,
        'residential_address': {
            'country': None,
            'state': None,
            'city': None,
            'town': None,
            'street': None,
            'house_num': None
        },
        'next_of_kin': {
            'first_name': None,
            'middle_name': None,
            'last_name': None,
            'relationship': None,
            'residential_address_country': None,
            'residential_address_state': None,
            'residential_address_city': None,
            'residential_address_town': None,
            'residential_address_email': None,
            'residential_address_telephone_num': None
        },
        'education': [],
        'certificates': [],
        'description': '',
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
        }
        med_user = self.collection.insert_one(new_practitioner)
        return med_user        

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def display_med_personnel(self):
        """display a brief profile of each medical personnel"""
        return list(self.collection.find({}, {'Personal_data': 1, 'Professional_data.description': 1}))

    def retrieve_form_format(self):
        """retrieve a collection from the db"""
        return self.collection.find_one()

    def insert(self, form_data):
        """create a new collection of medical experts"""
        personal_data = {
            "First_name": form_data.get('first_name', ""),
            "middle_name": form_data.get('middle_name', ""),
            "last_name": form_data.get('last_name', ""),
            "age": form_data.get('age', ""),
            "gender": form_data.get('gender', ""),
            "date_of_birth": form_data.get('date_of_birth', ""),
            "country_of_origin": form_data.get('country_of_origin', ""),
            "state_of_origin": form_data.get('state_of_origin', ""),
            "local_government_area": form_data.get('local_government_area', ""),
            "town_of_origin": form_data.get('town_of_origin', ""),
            "Email": form_data.get('email', ""),
            "mobile_num": form_data.get('mobile_num', ""),
            "LinkedIn": form_data.get('linkedin', ""),
            "Password": form_data.get('password', ""),
        }

        # Handle profile picture
        if 'profile_picture' in files:
            file = files['profile_picture']
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(self.UPLOAD_FOLDER, filename)
                file.save(file_path)
                personal_data["profile_picture"] = file_path

        residential_address = {
            "country": form_data.get('residential_address-country', ""),
            "state": form_data.get('residential_address-state', ""),
            "city": form_data.get('residential_address-city', ""),
            "town": form_data.get('residential_address-town', ""),
            "street": form_data.get('residential_address-street', ""),
            "house_num": form_data.get('residential_address-house_num', "")
        }

        next_of_kin = {
            "first_name": form_data.get('next_of_kin-first_name', ""),
            "middle_name": form_data.get('next_of_kin-middle_name', ""),
            "last_name": form_data.get('next_of_kin-last_name', ""),
            "relationship": form_data.get('next_of_kin-relationship', ""),
            "residential_address": {
                "country": form_data.get('next_of_kin-residential_address_country', ""),
                "state": form_data.get('next_of_kin-residential_address_state', ""),
                "city": form_data.get('next_of_kin-residential_address_city', ""),
                "town": form_data.get('next_of_kin-residential_address_town', ""),
                "email": form_data.get('next_of_kin-residential_address_email', ""),
                "telephone_num": form_data.get('next_of_kin-residential_address_telephone_num', "")
            }
        }

        professional_data = {
            "education": [],
            "certificates": [],
            "description": form_data.get('description', "")
        }

        # Handle education data
        for i in range(len(form_data.getlist('education-country'))):
            education_entry = {
                "country": form_data.getlist('education-country')[i],
                "university": form_data.getlist('education-university')[i],
                "degree": form_data.getlist('education-degree')[i]
            }
            professional_data["education"].append(education_entry)

        # Handle certificate data
        certificate_files = files.getlist('certificates-certificate_file')
        for i in range(len(form_data.getlist('certificates-certificate_type'))):
            file = certificate_files[i]
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(self.UPLOAD_FOLDER, filename)
                file.save(file_path)
                
                certificate_entry = {
                    "certificate_type": form_data.getlist('certificates-certificate_type')[i],
                    "certificate_file": file_path
                }
                professional_data["certificates"].append(certificate_entry)

        data = {
            "Personal_data": personal_data,
            "residential_address": residential_address,
            "Next_of_Kin": next_of_kin,
            "Professional_data": professional_data,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        self.collection.insert_one(data)