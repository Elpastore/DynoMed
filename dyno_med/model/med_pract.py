#!/usr/bin/env python
"""Module for all medical practitioners"""
from dyno_med import medical_practitioners
from datetime import datetime
from werkzeug.utils import secure_filename
from typing import List
import os
import re

class Medical:
    def __init__(self, med_user, data, files, username: str, first_name: str, middle_name: str,
                 last_name: str, age: int, gender: str, date_of_birth: datetime, country_of_origin: str,
                 state_of_origin: str, local_government_area: str, town_of_origin: str, email: str,
                 mobile_num: str, linkedin: str, password: str, residential_address: dict,
                 next_of_kin: dict, education: List, certificates: List, ....):
        """Initialize the Medical class"""
        self.UPLOAD_FOLDER = '/home/pc/DynoMed/dyno_med/file_DataBase'  # Set this to your desired upload path
        self.ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

        self.profile_picture = None
        self.username = None
        self.first_name = None
        self.middle_name = None
        self.last_name = None
        self.age = None
        self.gender = None
        self.date_of_birth = None
        self.country_of_origin = None
        self.state_of_origin = None
        self.local_government_area = None
        self.town_of_origin = None
        self.email = None
        self.mobile_num = None
        self.linkedin = None
        self.password = None
        self.residential_address = {}
        self.next_of_kin = {}
        self.education = []
        self.certificates = []

        # If data is provided, update the attributes
        if data:
            self.update_attributes(data)
        
        # If files are provided, handle them
        if files:
            self.handle_files(files)   
    
    def is_valid_email(email):
        """Check if the email is a valid one"""
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return email_regex.match(email) is not None

    @staticmethod
    def retrive_med_user(med_user_data: object) -> dict:
        """Retrive the medical user data from the database"""
        med_user = {
            'profile_picture_name': med_user_data.get('profile_picture_name') or '',
            'profile_picture_path': med_user_data.get('profile_picture_path') or '',
            'username': med_user_data.get('username') or '',
            'first_name': med_user_data.get('first_name') or '',
            'middle_name': med_user_data.get('middle_name') or '',
            'last_name': med_user_data.get('last_name') or '',
            'age': med_user_data.get('age') or '',
            'gender': med_user_data.get('gender') or '',
            'date_of_birth': med_user_data.get('date_of_birth') or '',
            'country_of_origin': med_user.data.get('country_of_origin') or '',
            'state_of_origin': med_user_data.get('state_of_origin') or '',
            'local_government_area': med_user_data.get('local_government_area') or '',
            'town_of_origin': med_user_data.get('town_of_origin') or '',
            'email': med_user_data.get('email') or '',
            'mobile_num': med_user_data.get('mobile_num') or '',
            'linkedin': med_user_data.get('linkedin') or '',
            'password': med_user_data.get('password') or '',
            'residential_address': {
                'country': med_user_data.get('residentiial_address', {}).get('country') or '',
                'state': med_user_data.get('residential_address', {}).get('state') or '',
                'city': med_user_data.get('residential_address', {}).get('city') or '',
                'town': med_user_data.get('residential_address', {}).get('state') or '',
                'street': med_user_data.get('residential_address', {}).get('street') or '',
                'house_num': med_user_data.get('residential_address', {}).get('house_num') or ''
                },

            # retrive the next of kin data from database
            'next_of_kin': {
                'first_name': med_user_data.get('next_of_kin', {}).get('first_name') or '',
                'middle_name': med_user_data.get('next_of_kin', {}).get('middle_name') or '',
                'last_name': med_user_data.get('next_of_kin', {}).get('last_name') or '',
                'relationship': med_user_data.get('next_of_kin', {}).get('relationship') or '',
                'residential_address_country': med_user_data.get('next_of_kin',{}).get('residential_address_country') or '',
                'residential_address_state': med_user_data.get('next_of_kin', {}).get('residential_address_state') or '',
                'residential_address_city': med_user_data.get('next_of_kin', {}).get('residential_address_city') or '',
                'residential_address_town': med_user_data.get('next_of_kin', {}).get('residential_address_town') or '',
                'residential_address_email': med_user_data.get('next_of_kin', {}).get('residential_address_email') or '',
                'residential_address_telephone_num': med_user_data.get('next_of_kin', {}).get('residential_address_telephone_num') or '',
                },
            
            # Retirve all education data of med_user from the database
            'education': [{
                    'country': edu.country if edu.country else '',
                    'university': edu.university if edu.university else '',
                    'degree': edu.degree if edu.degree else ''
                } for edu in med_user_data.get('education', [])],
            
            # Retirve the certifcate type, name and path from the database
            'certificates': [{
                'certificate_file_name': cert.certificate_file_name if cert.certificate_file_name else '',
                'certificate_type': cert.certificate_type if cert.certificate_type else '',
                'certificate_file_path': cert.certificate_file_path if cert.certificate_file_path else '',
            } for cert in med_user_data.get('certificates', [])]
        }
        return med_user

    def update_med_user(self, med_user, data, files):
        """ update the medical user data in the database from the form data"""
            
        # Extract the medcal expert data from the form
        # profile_picture = files.get('profile_picture')
        # if profile_picture:
        #    secure_pic = secure_filename(profile_picture.filename)
        #    picture_path = os.path.join('/home/pc/DynoMed/dyno_med/med_user/pic', secure_filename)
        #    profile_picture.save(picture_path)

        """Update attributes from provided data"""
        self.username = data.get('username')
        if not self.username:
            self.username = ''
        if not isinstance(self.username, str):
            raise TypeError('Username must be String')
        
        self.first_name = data.get('first_name')
        if not self.first_name:
            self.first_name = ''
        if not isinstance(self.first_name, str):
            raise TypeError('First Name must be string')
        
        self.middle_name = data.get('middle_name')
        if not self.middle_name:
            self.middle_name = ''
        if not isinstance(self.middle_name, str):
            raise TypeError('Middle Name must be string')
        
        self.last_name = data.get('last_name')
        if not self.last_name:
            self.last_name = ''
        if not isinstance(self.last_name, str):
            raise TypeError('Last Name must be string')
        
        self.age = data.get('age')
        if self.age:
            try:
                self.age = int(self.age)
            except ValueError:
                raise TypeError('Age must be an Integer')
        else:
            self.age = None

        self.gender = data.get('gender')
        if not self.gender:
            self.gender = ''
        if not isinstance(self.gender, str):
            raise TypeError('Gender must be string')
    
        self.date_of_birth = data.get('date_of_birth')
        if self.date_of_birth:
            try:
                self.date_of_birth = datetime.strptime(self.date_of_birth, '%Y-%m-%d') 
            except ValueError:
                raise TypeError('Date of birth must be in YYYY-MM-DD format')
        else:
            self.date_of_birth = None

        self.country_of_origin = data.get('country_of_origin')
        if not self.country_of_origin:
            self.country_of_origin = ''
        if not isinstance(self.country_of_origin, str):
            raise TypeError('Country of origin must be string')

        self.state_of_origin = data.get('state_of_origin')
        if not self.state_of_origin:
            self.state_of_origin = ''
        if not isinstance(self.state_of_origin, str):
            raise TypeError('State of origin must be string')
        
        self.local_government_area = data.get('local_government_area')
        if not self.local_government_area:
            self.local_government_area = ''
        if not isinstance(self.local_government_area, str):
            raise TypeError('Local government area must be string')
        
        self.town_of_origin = data.get('town_of_origin')
        if not self.town_of_origin:
            self.town_of_origin = ''
        if not isinstance(self.town_of_origin, str):
            raise TypeError('Town of origin must be string')
        
        self.email = data.get('email')
        if self.email:
            email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
            if not email_pattern.match(self.email):
                raise ValueError("Invalid email format")
        else:
            self.email = ''
else:
    self.email = ''
        self.mobile_num = data.get('mobile_num')
        self.linkedin = data.get('linkedin')
        self.password = data.get('password')
        # Extract the residential adress of med_expert which is an embeded doc in dbs
        residential_address = []
        country = data.get('residential_address.country')
        state = data.get('residential_address.state')
        city = data.get('residential_address.city')
        town = data.get('residential_address.town')
        house_num = data.get('residential_address.house_num')
        residential_address.append({
            'country': country,
            'state': state,
            'city': city,
            'town': town,
            'house_num': house_num
        })

        # Extract the next_of_kin data from the form
        next_of_kin = []
        next_of_kin_first_name = data.get('next_of_kin.first_name')
        next_of_kin_middle_name = data.get('next_of_kin.middle_name')
        next_of_kin_last_name = data.get('next_of_kin.last_name')
        next_of_kin_relationship = data.get('next_of_kin.relationship')
        next_of_kin_residential_address_country = data.get('next_of_kin.residential_address_country')
        next_of_kin_residential_address_state = data.get('next_of_kin.residential_address_state')
        next_of_kin_residential_address_city = data.get('next_of_kin.residential_address_city')
        next_of_kin_residential_address_town = data.get('next_of_kin.residential_address_town')
        next_of_kin_residential_address_email = data.get('next_of_kin.residential_address_email')
        next_of_kin_residential_address_telephone_num = data.get('next_of_kin.residential_address_telephone_num')
            # NexOfKin is an embeded doc in Expert
        next_of_kin.append({
            'first_name': next_of_kin_first_name,
            'middle_name': next_of_kin_middle_name,
            'last_name': next_of_kin_last_name,
            'relationship': next_of_kin_relationship,
            'residential_address_country': next_of_kin_residential_address_country,
            'residential_address_state': next_of_kin_residential_address_state,
            'residential_address_city': next_of_kin_residential_address_city,
            'residential_address_town': next_of_kin_residential_address_town,
            'residential_address_email': next_of_kin_residential_address_email,
            'residential_address_telephone_num': next_of_kin_residential_address_telephone_num
        })
        
        # Extract education data from the form(education is an ebeded doc in Expert)
        education = []
        index = 0
        while True:
            country_of_edu = data.get(f'education-{index}-country')
            versity_of_edu = data.get(f'education-{index}-university')
            degree_of_edu = data.get(f'education-{index}-degree')

            if not country_of_edu and not versity_of_edu and not degree_of_edu:
                break

            education.append({
                'country': country_of_edu,
                'university': versity_of_edu,
                'degree': degree_of_edu
            })
            index += 1
        
        # Extract the cert data fromthe form.(certificate is an embeded doc in Expert)
        certificates = []
        index = 0
        while True:
            certificate_type = data.get(f'certificate-{index}-type')
            certificate_file = files.get(f'certificate-{index}-file')
            if not certificate_type and not certificate_file:
                break
            if certificate_file:
                # Generate a safe filename
                filename = secure_filename(certificate_file.filename)
                # Define the path where the file will be saved
                file_path = os.path.join('/home/pc/DynoMed/dyno_med', filename)
                certificate_file.save(file_path) 
            certificates.append({
                'certificate_type': certificate_type,
                'certificate_file_name': filename,
                'certificate_file_path': file_path
            })
            index =+ 1

        # create the med_user object with the informations available
        med_user = Expert(
            profile_picture = profile_picture,
            username = username,
            first_name = first_name,
            middle_name = middle_name,
            last_name = last_name,
            age = age,
            gender = gender,
            date_of_birth = date_of_birth,
            country_of_origin = country_of_origin,
            state_of_origin = state_of_origin,
            local_government_area = local_government_area,
            town_of_origin = town_of_origin,
            email = email,
            mobile_num = mobile_num,
            linkedin = linkedin,
            password = password,
            residential_address = residential_address,
            next_of_kin = next_of_kin,
            education = education,
            certificates = certificates
        )
        med_user.save()

    except Exception as e:
        return jsonify({'meassage': str(e)}), 400
    
