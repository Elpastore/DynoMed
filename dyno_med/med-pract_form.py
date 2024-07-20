from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, SelectField, DateField,FieldList,
                     TextAreaField, FormField, FileField)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileAllowed

class ResidentialAddressForm(FlaskForm):
    country = StringField('Country', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    town = StringField('Town', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house_num = StringField('House Number', validators=[DataRequired()])

class NextOfKinForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    middle_name = StringField('Middle Name', validators=[Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    relationship = StringField('Relationship', validators=[DataRequired()])
    residential_address_country = StringField('Country', validators=[DataRequired()])
    residential_address_state = StringField('State', validators=[DataRequired()])
    residential_address_city = StringField('City', validators=[DataRequired()])
    residential_address_town = StringField('Town', validators=[DataRequired()])
    residential_address_email = StringField('Email', validators=[DataRequired(), Email()])
    residential_address_telephone_num = StringField('Telephone Number', validators=[DataRequired()])

class EducationForm(FlaskForm):
    country = SelectField('Country of Education', choices=[('US', 'United States'), ('UK', 'United Kingdom'), ('CA', 'Canada')], validators=[DataRequired()])
    university = StringField('University', validators=[DataRequired()])
    degree = StringField('Degree', validators=[DataRequired()])

class CertificateForm(FlaskForm):
    certificate_type = SelectField('Certificate Type', choices=[('degree', 'Degree Certificate'), ('professional', 'Professional Certificate'), ('training', 'Training Certificate'), ('other', 'Other')], validators=[DataRequired()])
    certificate_file = FileField('Upload Certificate', validators=[FileAllowed(['pdf', 'jpg', 'jpeg', 'png']), DataRequired()])

class ExpertRegistrationForm(FlaskForm):
    profile_picture = FileField('Upload Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png']), DataRequired()])
    
    # Personal Data
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    middle_name = StringField('Middle Name', validators=[Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    age = SelectField('Age', validators=[DataRequired()], choices=[(str(i), str(i)) for i in range(18, 80)])
    gender = SelectField('Gender', choices=[
        ('', 'Choose...'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say')
    ], validators=[DataRequired()])
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
    education = FieldList(FormField(EducationForm), min_entries=1)
    certificates = FieldList(FormField(CertificateForm), min_entries=1)
    description = TextAreaField('Professional Description', 
                                validators=[Optional()],
                                render_kw={"rows": 5, "placeholder": "Describe yourself, your specialties, and previous work experience (if any)"})


    submit = SubmitField('Register')

class ExpertLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ExpertResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ExpertResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')