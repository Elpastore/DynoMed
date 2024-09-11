#!/usr/bin/env python
"""Module for all medical practitioners"""
from datetime import datetime
from werkzeug.utils import secure_filename
from typing import List, Dict, Any, Optional
from dyno_med import (Expert, Education, Certificate, NextOfKin)
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


    @staticmethod
    def is_valid_email(email: str) -> bool:
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

    def handle_certificates(self, files: Optional[Dict[str, Any]], data: Dict[
        str, Any]) -> List[Dict[str, str]]:
        """
        Handle certificate uploads.

        Args:
            files (Dict[str, Any]): Dictionary containing file objects.
            data (Dict[str, Any]): Dictionary containing form data.

        Returns:
            List[Dict[str, str]]: List of dictionaries containing certificate information.

        Raises:
            ValueError: If an invalid file type is uploaded for a certificate.
        """
        for key in files:
            if key.startswith('certificate-') and key.endswith('-file'):
                file = files.get(key)
                if file.filename != '':
                    if self.allowed_file(file.filename):
                        index = key.split('-')[1]
                        cert_type = data.get(f'certificate-{index}-type')
                        filename = secure_filename(file.filename)
                        cert_path = os.path.join(self.UPLOAD_FOLDER, filename)
                        file.save(cert_path)
                        self.certificates.append({
                            'certificate_type': cert_type,
                            'certificate_file_name': filename,
                            'certificate_file_path': cert_path
                        })
                    else:
                        raise ValueError(f"Invalid file type for certificate: {file.filename}")
        return self.certificates

    ile type for profile picture")

    def update_residential_address(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Update residential address from data.

        Args:
            data (Dict[str, Any]): Dictionary containing form data.

        Returns:
            Dict[str, str]: Updated residential address dictionary.
        """
        if not data:
            raise TypeError('form Object not found!')
        self.residential_address = {
            'country': data.get('residential_address.country'),
            'state': data.get('residential_address.state'),
            'city': data.get('residential_address.city'),
            'town': data.get('residential_address.town'),
            'house_num': data.get('residential_address.house_num')
        }
        return self.residential_address
    
    def update_education(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Update residential address from data.

        Args:
            data (Dict[str, Any]): Dictionary containing form data.

        Returns:
            Dict[str, str]: Updated residential address dictionary.
        """
        if not data:
            raise TypeError('form Object not found!')
        self.residential_address = {
            'country': data.get('residential_address.country'),
            'state': data.get('residential_address.state'),
            'city': data.get('residential_address.city'),
            'town': data.get('residential_address.town'),
            'house_num': data.get('residential_address.house_num')
        }
        return self.residential_address

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

    def update_education(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Update education information from data.

        Args:
            data (Dict[str, Any]): Dictionary containing form data.

        Returns:
            List[Dict[str, str]]: Updated list of education dictionaries.
        """
        if not data:
            raise TypeError('form object not found!')
        self.education = []
        index = 0
        while True:
            country = data.get(f'education-{index}-country')
            university = data.get(f'education-{index}-university')
            degree = data.get(f'education-{index}-degree')
            if not country and not university and not degree:
                break
            self.education.append({
                'country': country,
                'university': university,
                'degree': degree
            })
            index += 1
        return self.education
    
    def check_input_params(self, med_user: object, data: Dict[str, Any],
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
        elif value is None:
            return ""  # or return None, depending on your preference
        elif isinstance(value, (int, float, bool)):
            return str(value)
        else:
            raise ValueError(f"Unexpected type for education data: {type(value)}")

    @staticmethod
    def update_med_user_education(self, med_user: object, education_data:
                                  Dict[str, any], _, user_id):
        """
        update the education information for the medical user

        :param med_user: The Expert document to update
        :param education_data: Dictionary containing the education from the data
        :param_: placeholder for files( not used)
        :param user_id: The ID of the user being updated 
        """
        self.check_input_params(med_user, education_data, _, user_id)
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
    
    @staticmethod
    def update_med_user_address(self, med_user: object, education_data:
                                Dict[str, any], _, user_id):
        """
        update the address information for the medical user

        :param med_user: The Expert document to update
        :param education_data: Dictionary containing the address from the data
        :param_: placeholder for files( not used)
        :param user_id: The ID of the user being updated 
        """
        self.check_input_params(med_user, education_data, _, user_id)
        

    @staticmethod
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