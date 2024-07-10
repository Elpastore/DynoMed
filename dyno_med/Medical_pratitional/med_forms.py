from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField, FormField, FieldList
from wtforms.validators import DataRequired, Length, Email, Regexp
from dyno_med import database
from dyno_med.Medical_pratitional import index_of_countries

countries = index_of_countries.african_countries_states

class AddressForm(FlaskForm):
    country = SelectField('Country', validators=[DataRequired()], choices=[(country, country), for country in countries.keys()])
    state = SelectField('State', validators=[DataRequired()], choices=[()])
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
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=30)])
    middle_name = StringField('Middle Name', validators=[Length(min=3, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=30)])
    age = SelectField('Age', validators=[DataRequired()], choices=[(num, num) for num in range(18, 60)])
    gender = SelectField('Gender', validators=[DataRequired()], choices=[("Male", "Male"), ("Female", "Female")])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    country_of_origin = SelectField('Country of Origin', validators=[DataRequired()], 
                                    choices=[(country, country) for country in countries.keys()])
    state_of_origin = SelectField('State of Origin', validators=[DataRequired()], choices=[])

    local_government_area = StringField('Local Government Area', validators=[DataRequired(), Length(min=2, max=50)])
    town_of_origin = StringField('Town of Origin', validators=[Length(max=50)])

    residential_address = FormField(AddressForm)

    next_of_kin_first_name = StringField('Next of Kin First Name', validators=[DataRequired(), Length(min=3, max=30)])
    next_of_kin_middle_name = StringField('Next of Kin Middle Name', validators=[Length(min=3, max=30)])
    next_of_kin_last_name = StringField('Next of Kin Last Name', validators=[DataRequired(), Length(min=3, max=30)])
    next_of_kin_relationship = StringField('Next of Kin Relationship', validators=[DataRequired(), Length(min=2, max=50)])
    next_of_kin_residential_address = FormField(AddressForm)

    profession = StringField('Profession', validators=[DataRequired(), Length(min=2, max=50)])
    primary_school = StringField('Primary School', validators=[Length(min=2, max=100)])
    high_school = StringField('High School', validators=[Length(min=2, max=100)])
    universities_colleges_attended = FieldList(FormField(EducationForm), min_entries=1)
    licenses = FieldList(StringField('License', validators=[Length(max=100)]), min_entries=1)
    cv = StringField('CV Path', validators=[Length(max=200)])
    certificates = FieldList(StringField('Certificate Path', validators=[Length(max=200)]), min_entries=1)

    submit = SubmitField('Submit')
        
