from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField, SelectField,
                     DateField, FieldList, FormField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from wtforms.fields import SelectMultipleField
from dyno_med import database
from forms import (RegistrationForm, LoginForm, ResetPasswordRequestForm)

# for importing file and validators
from flask_wtf.file import FileField, FileAllowed

class ExpertRegistrationForm(RegistrationForm):
    """registration class for all medical experts- inherits from """
    def __init__(self):
        """do nothing"""
        pass

    def validate_email(self, email):
        return super().validate_email(email)

class ExpertResetPasswordRequest(ResetPasswordRequestForm):
    """reset of the password, inherits from forms.py"""
    def __init__(self):
        """do nothing"""
        pass

    def validate_email(self, email):
        return super().validate_email(email)

class ExpertLoginForm(LoginForm):
    def __init__(self):
        pass

class ResidentialAddressForm(FlaskForm):
    country = StringField('Country', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    town = StringField('Town', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house_num = StringField('House Number', validators=[DataRequired()])

class NextOfKinAddressForm(FlaskForm):
    country = StringField('Country', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    town = StringField('Town', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telephone_num = StringField('Telephone Number', validators=[DataRequired()])

class NextOfKinForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    middle_name = StringField('Middle Name', validators=[Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    relationship = StringField('Relationship', validators=[DataRequired()])
    residential_address = FormField(NextOfKinAddressForm)

class EducationForm(FlaskForm):
    primary_school = StringField('Primary School')
    high_school = StringField('High School')
    university = FieldList(FormField(lambda: StringField('Institution')), min_entries=1)
    degree = FieldList(FormField(lambda: StringField('Degree')), min_entries=1)

class ProfessionalDataForm(FlaskForm):
    profession = StringField('Profession', validators=[DataRequired()])
    education = FormField(EducationForm)
    license = FieldList(StringField('License'), min_entries=1)
    cv = FileField('CV', validators=[FileAllowed(['pdf'])])
    certificates = FieldList(FileField('Certificate', validators=[FileAllowed(['pdf'])]), min_entries=1)

class ExpertupdateAccountForm(FlaskForm):
    """Update the expert account information"""
    # Personal Data
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    middle_name = StringField('Middle Name', validators=[Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    age = SelectField('Age', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()], format='%Y-%m-%d')
    country_of_origin = StringField('Country of Origin', validators=[DataRequired()])
    state_of_origin = StringField('State of Origin', validators=[DataRequired()])
    local_government_area = StringField('Local Government Area', validators=[DataRequired()])
    town_of_origin = StringField('Town of Origin', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mobile_num = StringField('Mobile Number', validators=[DataRequired()])
    linkedin = StringField('LinkedIn')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    # Residential Address
    residential_address = FormField(ResidentialAddressForm)

    # Next of Kin
    next_of_kin = FormField(NextOfKinForm)

    # Professional Data
    professional_data = FormField(ProfessionalDataForm)

    submit = SubmitField('Update Account')
