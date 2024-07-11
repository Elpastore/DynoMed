#!/usr/bin/env python
"""module for all medical pratitioners"""
from flask import Flask, jsonify

class Medical:
    def __init__(self) -> None:
        """do nothing here"""
        pass
    
    def insert_db(form):
        """Insert new record into the medical personnel database"""
        first_name = form.first_name.data
        middle_name = form.middle_name.data
        last_name = form.last_name.data
        age = form.age.data
        gender = form.gender.data
        date_of_birth = form.date_of_birth.data
        country_of_origin = form.country_of_origin.data
        state_of_origin = form.state_of_origin.data
        local_government_area = form.local_government_area.data
        town_of_origin = form.town_of_origin.data

        residential_address = {
            "country": form.residential_address.country.data,
            "state": form.residential_address.state.data,
            "city": form.residential_address.city.data,
            "town": form.residential_address.town.data,
            "street": form.residential_address.street.data,
            "house_num": form.residential_address.house_num.data,
            "email": form.residential_address.email.data,
            "telephone_num": form.residential_address.telephone_num.data,
        }

        next_of_kin = {
            "first_name": form.next_of_kin_first_name.data,
            "middle_name": form.next_of_kin_middle_name.data,
            "last_name": form.next_of_kin_last_name.data,
            "relationship": form.next_of_kin_relationship.data,
            "address": {
                "country": form.next_of_kin_residential_address.country.data,
                "state": form.next_of_kin_residential_address.state.data,
                "city": form.next_of_kin_residential_address.city.data,
                "town": form.next_of_kin_residential_address.town.data,
                "street": form.next_of_kin_residential_address.street.data,
                "house_num": form.next_of_kin_residential_address.house_num.data,
                "email": form.next_of_kin_residential_address.email.data,
                "telephone_num": form.next_of_kin_residential_address.telephone_num.data,
            }
        }

        profession = form.profession.data
        primary_school = form.primary_school.data
        high_school = form.high_school.data
        universities_colleges_attended = [{"institution": edu.institution.data, "degree": edu.degree.data} for edu in form.universities_colleges_attended]
        licenses = [license.data for license in form.licenses]
        cv = form.cv.data
        certificates = [certificate.data for certificate in form.certificates]

        new_medical_practitioner = database['medical_practitioners'].insert_one({
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'age': age,
            'gender': gender,
            'date_of_birth': date_of_birth,
            'country_of_origin': country_of_origin,
            'state_of_origin': state_of_origin,
            'local_government_area': local_government_area,
            'town_of_origin': town_of_origin,
            'residential_address': residential_address,
            'next_of_kin': next_of_kin,
            'profession': profession,
            'primary_school': primary_school,
            'high_school': high_school,
            'universities_colleges_attended': universities_colleges_attended,
            'licenses': licenses,
            'cv': cv,
            'certificates': certificates
        })

        return jsonify({'message': f'Medical practitioner registration successful! ID: {new_medical_practitioner.inserted_id}'})
