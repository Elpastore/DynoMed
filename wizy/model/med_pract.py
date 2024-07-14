#!/usr/bin/env python
"""module for all medical pratitioners"""
from . import database
from datetime import date

class Medical:
    def __init__(self) -> None:
        """do nothing here"""
        pass

    def display_med_personel():
        """display a brief profile of each medical personel"""
    
    def retrieve_form_format():
        """retrieve a collection from the db"""
        return database.medical_practitioner
    
    def insert(self, form_data):
        """craete a new collection of medical experrts"""
        personal_data = {
            "First_name": form_data.get('first_name', ""),
            "middle_name": form_data.get('middle_name', ""),
            "last_name": form_data.get('last_name', ""),
            "age": None,
            "date_of_birth": form_data.get('date_of_birth', ""),
            "country_of_origin": form_data.get('country_of_origin', ""),
            "state_of_origin": form_data.get('state_of_origin', ""),
            "local_government_area": form_data.get('local_government_area', ""),
            "town_of_origin": form_data.get('town_of_origin', ""),
            "Email": form_data.get('email', ""),
            "mobile_num": form_data.get('mobile_num', ""),
            "LinkedIn": form_data.get('linkedIn', ""),
            "Password": form_data.get('passWord', ""),
            "confirm_password ": form_data.get('confirm_password', "")
        }
        
        residential_address = {
            "country": form_data.get('residential_country', ""),
            "state": form_data.get('residential_state', ""),
            "city": form_data.get('residential_city', ""),
            "town": form_data.get('residential_town', ""),
            "street": form_data.get('residential_street', ""),
            "house_num": form_data.get('residential_house_num', "")
        }
        
        next_of_kin = {
            "first_name": form_data.get('nok_first_name', ""),
            "middle_name": form_data.get('nok_middle_name', ""),
            "last_name": form_data.get('nok_last_name', ""),
            "relationship": form_data.get('nok_relationship', ""),
            "residential_address": {
                "country": form_data.get('nok_residential_country', ""),
                "state": form_data.get('nok_residential_state', ""),
                "city": form_data.get('nok_residential_city', ""),
                "town": form_data.get('nok_residential_town', ""),
                "email": form_data.get('nok_email', ""),
                "telephone_num": form_data.get('nok_telephone_num', "")
            }
        }
        
        professional_data = {
            "profession": form_data.get('profession', ""),
            "education": {
                "primary_school": form_data.get('primary_school', ""),
                "high_school": form_data.get('high_school', ""),
                "university": [
                    {"institution": form_data.get('university_1_institution', ""), "degree": form_data.get('university_1_degree', "")},
                    {"institution": form_data.get('university_2_institution', ""), "degree": form_data.get('university_2_degree', "")}
                ]
            },
            "license": [
                form_data.get('license_1', ""), 
                form_data.get('license_2', ""), 
                form_data.get('license_3', ""), 
                form_data.get('license_4', "")
            ],
            "cv": form_data.get('cv', "path/to/cv.pdf"),
            "certificates": [
                form_data.get('certificate_1', "path/to/certificate1.pdf"),
                form_data.get('certificate_2', "path/to/certificate2.pdf")
            ]
        }

        data = {
            "Personal_data": personal_data,
            "residential_address": residential_address,
            "Next_of_Kin": next_of_kin,
            "Professional_data": professional_data
        }

        database.medical_practitioners.insert_one(data)