#!/usr/bin/env python
"""Module for all medical practitioners"""
from datetime import datetime
from werkzeug.utils import secure_filename
from typing import List, Dict, Any, Optional
from dyno_med import (Expert, Education, Experience, Certificate, NextOfKin)
from bson import ObjectId
import os
import re

class Medical:
    """
    A class to handle medical practitioner information and file uploads.
    """

    def __init__(self, med_user: Optional[Any] = None, data: Optional[Dict[str, Any]] = None,
                 files: Optional[Dict[str, Any]] = None):
        """
        Initialize the Medical class.

        Args:
            med_user (Optional[Any]): The medical user object.
            data (Optional[Dict[str, Any]]): Dictionary containing user data.
            files (Optional[Dict[str, Any]]): Dictionary containing file objects.
        """
        self.UPLOAD_FOLDER: str = '/home/pc/DynoMed/dyno_med/file_DataBase/certificate'
        self.UPLOAD_PIC: str = '/home/pc/DynoMed/dyno_med/file_DataBase/Picture'
        self.ALLOWED_EXTENSIONS: List[str] = ['jpg', 'jpeg', 'png']

        self.profile_picture: Optional[str] = None
        self.username: Optional[str] = None
        self.first_name: Optional[str] = None
        self.middle_name: Optional[str] = None
        self.last_name: Optional[str] = None
        self.age: Optional[int] = None
        self.gender: Optional[str] = None
        self.date_of_birth: Optional[datetime] = None
        self.country_of_origin: Optional[str] = None
        self.state_of_origin: Optional[str] = None
        self.local_government_area: Optional[str] = None
        self.town_of_origin: Optional[str] = None
        self.email: Optional[str] = None
        self.mobile_num: Optional[int] = None
        self.linkedin: Optional[str] = None
        self.password: Optional[str] = None
        self.residential_address: Dict[str, str] = {}
        self.next_of_kin: Dict[str, str] = {}
        self.education: List[Dict[str, str]] = []
        self.certificates: List[Dict[str, str]] = []

    def is_valid_email(self, email: str) -> bool:
        """
        Check if the email is valid.

        Args:
            email (str): The email to validate.

        Returns:
            bool: True if the email is valid, False otherwise.
        """
        if not email:
            raise ValueError('Email field is empty')
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return email_regex.match(email) is not None

    def allowed_file(self, filename: str) -> bool:
        """
        Check if the file extension is allowed.

        Args:
            filename (str): The name of the file to check.

        Returns:
            bool: True if the file extension is allowed, False otherwise.
        """
        if not filename:
            raise
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    

    ile type for profile picture")

    
    

    def update_next_of_kin(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Update next of kin information from data.

        Args:
            data (Dict[str, Any]): Dictionary containing form data.

        Returns:
            Dict[str, str]: Updated next of kin dictionary.
        """
        if not data:
            raise ValueError('form object not found')
        self.next_of_kin = {
            'first_name': data.get('next_of_kin.first_name'),
            'middle_name': data.get('next_of_kin.middle_name'),
            'last_name': data.get('next_of_kin.last_name'),
            'relationship': data.get('next_of_kin.relationship'),
            'residential_address_email': data.get('next_of_kin.residential_address_email'),
            'residential_address_telephone_num': data.get('next_of_kin.residential_address_telephone_num')
        }
        return self.next_of_kin

    
    
    def _check_input_params(self, med_user: object, data: Dict[str, Any],
                               files: Optional[Dict[str, Any]], user_id):
            if not med_user:
                raise ValueError('No user found, ''please provide medical user''')
            if not data:
                raise ValueError('No form data found, pleade provide the object from the databse')
            if files == None:
                pass
            elif not files:
                raise ValueError('No files data found')
            if not user_id:
                raise ValueError('No user id found: please provide user id')
    
    def _ensure_string(self, value):
        """
        Ensure the given value is a string.
        
        :param value: The value to check and potentially convert
        :return: The value as a string
        """
        if isinstance(value, str):
            return value
        elif value == '':
            return ""  # or return None, depending on your preference
        elif isinstance(value, (int, float, bool)):
            return str(value)
        else:
            raise ValueError(f"Unexpected type for education data: {type(value)}")
    
    def _ensure_date(self, value):
        """
        Ensure the given value is a string.
        :param value: The value to check and convert to date format
        :param return: return the value in dat format
        """
        if not isinstance(value, datetime):
            if value == '':
                return ''
            try:
                value = datetime.strptime(value, '%m-%d-%Y')
            except Exception as e:
                print(f"Error in date conversion: {e}")

    def _handle_fullName(self, fullname: str) -> List:
        """
        Extract the first name, middle name and last name from the full name

        Args:
            fullname: A string containing the fullname of the user
        
        Return: Returns a list containing the first name, middlename(if exist)
                and last name of the user
        """
        try:
            value = self._ensure_string(fullname)
            if value == '':
                first_name = ''
                middle_name = ''
                last_name = ''
            name_segments = fullname.split()
            if len(name_segments) == 1:
                first_name, middle_name, last_name = name_segments, '', ''
            elif len(name_segments) == 2:
                first_name, last_name = name_segments
                middle_name = ''
            elif len(name_segments) >= 3:
                first_name, middle_name, last_name = name_segments[0], ''.join(name_segments[1:-1]),
                name_segments[-1]
            return [first_name, middle_name, last_name]
        except Exception as e:
            raise Exception(f"failed to extract names from full name: {e}")

    def _handle_address(self, address: str) -> List:
        """
        Extract the street, city and state from the address

        Args:
            address: A string containing the adress of the user
        
        Return: Returns a list containing the street, city(if exist)
                and state of the user
        """
        address = self._ensure_string(address)
        if address == '':
            street, city, state, country = '', '', '', ''
        adress_index = address.split(',')
        if len(adress_index) == 3:
            street, city, state, country = adress_index[0], adress_index[1], adress_index[-1], ''
        elif len(adress_index) == 4:
            street, city, state, country = adress_index[0], adress_index[1],
            adress_index[2],adress_index[-1]
        return [street, city, state, country]
    
    def _handle_num(self, number) -> List:
        """
        Extract the number and arrange the number including the country code in the database

        Args:
            number: the number plus the country code from the form object
        
        Return: Return a list contain ing the number and the country code
        """
        number_box = []
        new_box = []
        if number == '':
            return ''
        if not number:
            return
        number_box = number.split()
        for i in number_box:
            for j in range(len(number_box)):
                if type(i) is not int:
                    index = int(i)
                new_box[j] = index
        return new_box
        


    def update_med_user_experience(self, med_user: object,
                                   experience_data: Dict[str, any], _, user_id):
        """
        update the experience information for the medical user

        :param med_user: The Expert document to update
        :param experience_data: Dictionary containing the education from the data
        :param_: placeholder for files( not used)
        :param user_id: The ID of the user being updated
        """
        self._check_input_params(med_user, experience_data, _, user_id)
        try:
            # process experience data
            new_experience = []
            for index in range(len(experience_data['company'])):
                experience = Experience(
                    company=self._ensure_string(experience_data['company'][index]),
                    role=self._ensure_string(experience_data['role'][index]),
                    start_date=self._ensure_date(experience_data['startDate'][index]),
                    end_date=self._ensure_date(experience_data['endDate'][index])
                )
            new_experience.append(experience)
            med_user.experience = new_experience
            med_user.save()
        except Exception as e:
            print(f"Error updating experience for user {user_id}: {str(e)}")
            raise Exception(f"Failed to update experience: {str(e)}")


    def update_med_user_education(self, med_user: object, education_data:
                                  Dict[str, any], _, user_id):
        """
        update the education information for the medical user

        :param med_user: The Expert document to update
        :param education_data: Dictionary containing the education from the data
        :param_: placeholder for files( not used)
        :param user_id: The ID of the user being updated 
        """
        self._check_input_params(med_user, education_data, _, user_id)
        try:
            # process education data
            new_education = []
            for index in range(len(education_data['university'])):
                education = Education(
                    university=self._ensure_string(education_data['university'][index]),
                    course=self._ensure_string(education_data['course'][index]),
                    entry_yr=self._ensure_string(education_data['entryYear'][index]),
                    completion_yr=self._(education_data['endYear'][index]),
                    degree=self._ensure_string(education_data['degree'][index])
                )
                new_education.append(education)

            #update the users education
            med_user.education = new_education
            med_user.save()
        except Exception as e:
            print(f"Error updating education for user {user_id}: {str(e)}")
            raise Exception(f"Failed to update education: {str(e)}")
    
    def update_med_user_address(self, med_user: object, address_data:
                                Dict[str, any], _, user_id):
        """
        update the address information for the medical user

        :param med_user: The Expert document to update
        :param education_data: Dictionary containing the address from the data
        :param_: placeholder for files( not used)
        :param user_id: The ID of the user being updated 
        """
        self._check_input_params(med_user, address_data, _, user_id)
        try:
            # update the specified field only
            med_user.country_of_origin = self._ensure_string(address_data.get('country_of_origin'))
            med_user.state_of_origin = self._ensure_string(address_data.get('sate_of_origin'))
            med_user.local_government_area = self._ensure_string(address_data.get('local_government_area'))
            med_user.town_of_origin = self._ensure_string(address_data.get('town_of_origin'))

            # save the updated document
            med_user.save()
        except Exception as e:
            print(f"Error updating address for user {med_user.id}: {str(e)}")
            raise Exception(f"Failed to update: {str(e)}")
    
    def med_user_kin(self, med_user: object, kin_data: 
                     Dict[str, any], _, user_id):
        """
        Update the next of kin data in db from the next_of_kin_ form

        Args:
            med_user: the Expert document to update
            kin_data: The dictionary containg the next of kin data from the form
            user_: the id of the med_uer

        Return:
            retun None
        """
        self._check_input_params(med_user, kin_data, _, user_id)
        name_list = []
        fullname = kin_data['KinName']
        address = kin_data['address']
        name_list = self._handle_fullName(fullname)
        first_name, middle_name, last_name = name_list

        address_list = self._handle_address(address)
        street, city, state, country = address_list

        try:
            next_of_kin = NextOfKin(
                first_name=self.ensure_string(first_name),
                middle_name=self.ensure_string(middle_name),
                last_name=self.ensure_string(last_name),
                relationship=self._ensure_string(kin_data['relationship']),
                residential_address_email=kin_data['email'],
                residential_address_telephone_num=self._handle_num(kin_data['number']),
                residential_address_country=self._ensure_string(country),
                residential_address_state=self._ensure_string(state), 
                residential_address_city=self._ensure_string(city),
                residential_address_street=self._ensure_string(street)
            )
            med_user.next_of_kin = next_of_kin
            med_user.save()
        except Exception as e:
            raise Exception(f"could not update the next_of_kin in database: {e}")

    def retrive_med_user(med_user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve the medical user data from the database.

        Args:
            med_user_data (Dict[str, Any]): Dictionary containing medical user data.

        Returns:
            Dict[str, Any]: Formatted medical user data.
        """
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
            'country_of_origin': med_user_data.get('country_of_origin') or '',
            'state_of_origin': med_user_data.get('state_of_origin') or '',
            'local_government_area': med_user_data.get('local_government_area') or '',
            'town_of_origin': med_user_data.get('town_of_origin') or '',
            'email': med_user_data.get('email') or '',
            'mobile_num': med_user_data.get('mobile_num') or '',
            'linkedin': med_user_data.get('linkedin') or '',
            'password': med_user_data.get('password') or '',
            'residential_address': {
                'country': med_user_data.get('residential_address', {}).get('country') or '',
                'state': med_user_data.get('residential_address', {}).get('state') or '',
                'city': med_user_data.get('residential_address', {}).get('city') or '',
                'town': med_user_data.get('residential_address', {}).get('town') or '',
                'street': med_user_data.get('residential_address', {}).get('street') or '',
                'house_num': med_user_data.get('residential_address', {}).get('house_num') or ''
                },
            'next_of_kin': {
                'first_name': med_user_data.get('next_of_kin', {}).get('first_name') or '',
                'middle_name': med_user_data.get('next_of_kin', {}).get('middle_name') or '',
                'last_name': med_user_data.get('next_of_kin', {}).get('last_name') or '',
                'relationship': med_user_data.get('next_of_kin', {}).get('relationship') or '',
                'residential_address_email': med_user_data.get('next_of_kin', {}).get('residential_address_email') or '',
                'residential_address_telephone_num': med_user_data.get('next_of_kin', {}).get('residential_address_telephone_num') or '',
                },
            'education': [{
                    'country': edu.get('country') if edu.get('country') else '',
                    'university': edu.get('university') if edu.get('university') else '',
                    'degree': edu.get('degree') if edu.get('degree') else ''
                } for edu in med_user_data.get('education', [])],
            'certificates': [{
                'certificate_file_name': cert.get('certificate_file_name') if cert.get('certificate_file_name') else '',
                'certificate_type': cert.get('certificate_type') if cert.get('certificate_type') else '',
                'certificate_file_path': cert.get('certificate_file_path') if cert.get('certificate_file_path') else '',
            } for cert in med_user_data.get('certificates', [])],
            'description': med_user_data.get('description') or '',
        }
        print(med_user)
        return med_user