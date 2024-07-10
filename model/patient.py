#!/usr/bin/python3
# from dyno_med import record
from mongoengine import  Document, EmbeddedDocument, StringField, ListField, EmbeddedDocumentField, DateTimeField, IntField, FloatField, DateField
from datetime import datetime
from mongoengine import connect

connect('Record', host='mongodb://127.0.0.1:27017/Record')


class VitalSigns(EmbeddedDocument):
    blood_pressure = StringField()
    heart_rate = IntField()
    temperature = FloatField()
    respiration_rate = IntField()

class Medication(EmbeddedDocument):
    name= StringField()
    dosage = StringField()
    start_date = DateField()
    end_date  = DateField()

class Surgery(EmbeddedDocument):
    procedure = StringField(required=True)
    date = DateField()
    outcome = StringField()

class Allergy(EmbeddedDocument):
    name = StringField(required=True)
    reaction = StringField()

class MedicalRecord(EmbeddedDocument):
    chief_complaint = StringField()
    symptoms = ListField(StringField())
    diagnoses = ListField(StringField())
    vital_signs = EmbeddedDocumentField(VitalSigns)
    medications = ListField(EmbeddedDocumentField(Medication))
    surgeries = ListField(EmbeddedDocumentField(Surgery))
    allergies = ListField(EmbeddedDocumentField(Allergy))
    



class Laboratory(EmbeddedDocument):
    test_name = StringField()
    result = StringField()
    pathology_reports = StringField()

class Patient(Document):
    full_name = StringField(required=True)
    birthday = DateField(require=True)
    gender = StringField(required=True)
    contact_information = StringField()
    emergency_contact = StringField()
    medical_history = ListField(EmbeddedDocumentField(MedicalRecord))
    current_health_information = EmbeddedDocumentField(MedicalRecord)
    immunization_records = ListField(StringField())
    insurance_information = StringField()
    