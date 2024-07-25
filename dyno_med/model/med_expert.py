#!/usr/bin/env python3
from mongoengine import Document, EmbeddedDocument, StringField, ListField, EmbeddedDocumentField, DateTimeField, IntField, DateField, FileField, EmailField
from datetime import datetime
from mongoengine import connect

# connect('Expert', host='mongodb://127.0.0.1:27017/Expert')

class ResidentialAddress(EmbeddedDocument):
    country = StringField(required=True)
    state = StringField(required=True)
    city = StringField(required=True)
    town = StringField(required=True)
    street = StringField(required=True)
    house_num = StringField(required=True)

class NextOfKin(EmbeddedDocument):
    first_name = StringField(required=True, min_length=2, max_length=50)
    middle_name = StringField(max_length=50)
    last_name = StringField(required=True, min_length=2, max_length=50)
    relationship = StringField(required=True)
    residential_address_country = StringField(required=True)
    residential_address_state = StringField(required=True)
    residential_address_city = StringField(required=True)
    residential_address_town = StringField(required=True)
    residential_address_email = EmailField(required=True)
    residential_address_telephone_num = StringField(required=True)

class Education(EmbeddedDocument):
    country = StringField(required=True, choices=['US', 'UK', 'CA'])
    university = StringField(required=True)
    degree = StringField(required=True)

class Certificate(EmbeddedDocument):
    certificate_type = StringField(required=True, choices=['degree', 'professional', 'training', 'other'])
    certificate_file = FileField(required=True)

class Expert(Document):
    profile_picture = FileField(required=True)
    
    # Personal Data
    username = StringField(required=True, min_length=2, max_length=50)
    first_name = StringField(required=True, min_length=2, max_length=50)
    middle_name = StringField(max_length=50)
    last_name = StringField(required=True, min_length=2, max_length=50)
    age = IntField(required=True, min_value=18, max_value=79)
    gender = StringField(required=True, choices=['male', 'female', 'other', 'prefer_not_to_say'])
    date_of_birth = DateField(required=True)
    country_of_origin = StringField(required=True)
    state_of_origin = StringField(required=True)
    local_government_area = StringField(required=True)
    town_of_origin = StringField(required=True)
    email = EmailField(required=True)
    mobile_num = StringField(required=True)
    linkedin = StringField()
    passWord = StringField()

    # Residential Address
    residential_address = EmbeddedDocumentField(ResidentialAddress, required=True)

    # Next of Kin
    next_of_kin = EmbeddedDocumentField(NextOfKin, required=True)

    # Professional Data
    education = ListField(EmbeddedDocumentField(Education), required=True)
    certificates = ListField(EmbeddedDocumentField(Certificate), required=True)
    description = StringField()

    # Metadata
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'experts',
        'indexes': ['username', 'email']
    }

class ExpertLogin(Document):
    email = EmailField(required=True)
    password = StringField(required=True)  # Note: In practice, store hashed passwords

class ExpertPasswordResetRequest(Document):
    email = EmailField(required=True)

class ExpertPasswordReset(Document):
    password = StringField(required=True)
    confirm_password = StringField(required=True)