#!/usr/bin/env python3
"""Doctors module"""
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, IntegerField, DateField, 
                     FieldList, FormField, SelectField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from dyno_med import database
from Index_of_countries import african_countries_states as african

class AddressForm(FlaskForm):
    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=50)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=50)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=50)])
    town = StringField('Town', validators=[Length(max=50)])
    street = StringField('Street', validators=[Length(max=100)])
    house_num = StringField('House Number', validators=[Length(max=10)])
    email = StringField('Email', validators=[Email(), Length(max=100)])
    telephone_num = StringField('Telephone Number', validators=[DataRequired(), Regexp(r'^\d{7,15}$', message="Invalid telephone number")])

class EducationForm(FlaskForm):
    institution = StringField('Institution', validators=[DataRequired(), Length(min=2, max=100)])
    degree = StringField('Degree', validators=[DataRequired(), Length(min=2, max=50)])

class MedicalPersonel(FlaskForm):
    # Personal Data
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=30)])
    middle_name = StringField('Middle Name', validators=[Length(min=3, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=30)])
    age = IntegerField('Age', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    country_of_origin = SelectField('Country of Origin', validators=[DataRequired()],
                                    choices=[(country, country) for country, states in african.items()])
    state_of_origin = StringField('State of Origin', validators=[DataRequired(), Length(min=2, max=50)])
    local_government_area = StringField('Local Government Area', validators=[DataRequired(), Length(min=2, max=50)])
    town_of_origin = StringField('Town of Origin', validators=[Length(max=50)])

    # Residential Address
    residential_address = FormField(AddressForm)

    # Next of Kin
    next_of_kin_first_name = StringField('Next of Kin First Name', validators=[DataRequired(), Length(min=3, max=30)])
    next_of_kin_middle_name = StringField('Next of Kin Middle Name', validators=[Length(min=3, max=30)])
    next_of_kin_last_name = StringField('Next of Kin Last Name', validators=[DataRequired(), Length(min=3, max=30)])
    next_of_kin_relationship = StringField('Next of Kin Relationship', validators=[DataRequired(), Length(min=2, max=50)])
    next_of_kin_residential_address = FormField(AddressForm)

    # Professional Data
    profession = StringField('Profession', validators=[DataRequired(), Length(min=2, max=50)])
    primary_school = StringField('Primary School', validators=[Length(min=2, max=100)])
    high_school = StringField('High School', validators=[Length(min=2, max=100)])
    universities_colleges_attended = FieldList(FormField(EducationForm), min_entries=1)
    licenses = FieldList(StringField('License', validators=[Length(max=100)]), min_entries=1)
    cv = StringField('CV Path', validators=[Length(max=200)])
    certificates = FieldList(StringField('Certificate Path', validators=[Length(max=200)]), min_entries=1)

    # Submit
    submit = SubmitField('Submit')

    def validate_personal_data(self):
        """Validate personal data fields."""
        if not isinstance(self.first_name.data, str):
            raise TypeError("First name must be a string")
        if self.middle_name.data and not isinstance(self.middle_name.data, str):
            raise TypeError("Middle name must be a string")
        if not isinstance(self.last_name.data, str):
            raise TypeError("Last name must be a string")
        if not isinstance(self.age.data, int):
            raise TypeError("Age must be an integer")

    def validate_address(self, address_form):
        """Validate address fields."""
        if not isinstance(address_form.country.data, str):
            raise TypeError("Country must be a string")
        if not isinstance(address_form.state.data, str):
            raise TypeError("State must be a string")
        if not isinstance(address_form.city.data, str):
            raise TypeError("City must be a string")
        if address_form.town.data and not isinstance(address_form.town.data, str):
            raise TypeError("Town must be a string")
        if address_form.street.data and not isinstance(address_form.street.data, str):
            raise TypeError("Street must be a string")
        if address_form.house_num.data and not isinstance(address_form.house_num.data, str):
            raise TypeError("House number must be a string")
        if address_form.telephone_num.data and not isinstance(address_form.telephone_num.data, str):
            raise TypeError("Telephone number must be a string")
        if not isinstance(address_form.email.data, str):
            raise TypeError("Email must be a string")

    def validate_next_of_kin(self):
        """Validate next of kin fields."""
        if not isinstance(self.next_of_kin_first_name.data, str):
            raise TypeError("Next of Kin first name must be a string")
        if self.next_of_kin_middle_name.data and not isinstance(self.next_of_kin_middle_name.data, str):
            raise TypeError("Next of Kin middle name must be a string")
        if not isinstance(self.next_of_kin_last_name.data, str):
            raise TypeError("Next of Kin last name must be a string")
        if not isinstance(self.next_of_kin_relationship.data, str):
            raise TypeError("Next of Kin relationship must be a string")
        self.validate_address(self.next_of_kin_residential_address)

    def validate_professional_data(self):
        """Validate professional data fields."""
        if not isinstance(self.profession.data, str):
            raise TypeError("Profession must be a string")
        if self.primary_school.data and not isinstance(self.primary_school.data, str):
            raise TypeError("Primary school must be a string")
        if self.high_school.data and not isinstance(self.high_school.data, str):
            raise TypeError("High school must be a string")
        for entry in self.universities_colleges_attended.entries:
            if not isinstance(entry.form.institution.data, str):
                raise TypeError("Institution must be a string")
            if not isinstance(entry.form.degree.data, str):
                raise TypeError("Degree must be a string")
        for license in self.licenses.entries:
            if not isinstance(license.data, str):
                raise TypeError("License must be a string")
        if self.cv.data and not isinstance(self.cv.data, str):
            raise TypeError("CV Path must be a string")
        for certificate in self.certificates.entries:
            if not isinstance(certificate.data, str):
                raise TypeError("Certificate Path must be a string")
