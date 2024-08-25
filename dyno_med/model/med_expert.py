#!/usr/bin/env python3
from mongoengine import Document, EmbeddedDocument, StringField, ListField, EmbeddedDocumentField, DateTimeField, IntField, DateField, FileField, EmailField
from datetime import datetime
from mongoengine import connect

# connect('Expert', host='mongodb://127.0.0.1:27017/Expert')

class ResidentialAddress(EmbeddedDocument):
    country = StringField(required=False)
    state = StringField(required=False)
    city = StringField(required=False)
    town = StringField(required=False)
    street = StringField(required=False)
    house_num = StringField(required=False)

class NextOfKin(EmbeddedDocument):
    first_name = StringField(required=False, min_length=2, max_length=50)
    middle_name = StringField(max_length=50)
    last_name = StringField(required=False, min_length=2, max_length=50)
    relationship = StringField(required=False)
    residential_address_country = StringField(required=False)
    residential_address_state = StringField(required=False)
    residential_address_city = StringField(required=False)
    residential_address_town = StringField(required=False)
    residential_address_email = EmailField(required=False)
    residential_address_telephone_num = StringField(required=False)

class Education(EmbeddedDocument):
    country = StringField(required=False, choices=['US', 'UK', 'CA'])
    university = StringField(required=False)
    degree = StringField(required=False)

class Certificate(EmbeddedDocument):
    certificate_type = StringField(required=False, choices=['degree', 'professional', 'training', 'other'])
    certificate_file_name = StringField(required=False)
    certificate_file_path = StringField(required=False)

class Expert(Document):
    # Personal Data
    profile_picture_name = StringField(required=False)
    profile_picture_path = StringField(require=False)
    username = StringField(min_length=2, max_length=50)
    first_name = StringField(min_length=2, max_length=50)
    middle_name = StringField(max_length=50)
    last_name = StringField(min_length=2, max_length=50)
    age = IntField(min_value=18, max_value=79)
    gender = StringField(choices=['male', 'female', 'other', 'prefer_not_to_say'])
    date_of_birth = DateField(required=False)
    country_of_origin = StringField(required=False)
    state_of_origin = StringField(required=False)
    local_government_area = StringField(required=False)
    town_of_origin = StringField(required=False)
    email = EmailField(required=False)
    mobile_num = StringField(required=False)
    linkedin = StringField()
    passWord = StringField()

    # Residential Address
    residential_address = EmbeddedDocumentField(ResidentialAddress, required=False)

    # Next of Kin
    next_of_kin = EmbeddedDocumentField(NextOfKin, required=False)

    # Professional Data
    education = ListField(EmbeddedDocumentField(Education), required=False)
    certificates = ListField(EmbeddedDocumentField(Certificate), required=False)
    description = StringField()

    # Metadata
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'medical_practitioners',
        'db_alias': 'default',
        'indexes': ['username', 'email']
    }

class ExpertLogin(Document):
    email = EmailField(required=False)
    password = StringField(required=False)  # Note: In practice, store hashed passwords

class ExpertPasswordResetRequest(Document):
    email = EmailField(required=False)

class ExpertPasswordReset(Document):
    password = StringField(required=False)
    confirm_password = StringField(required=False)