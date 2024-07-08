#!/usr/bin/python3
from dyno_med import record
from mongoengine import  Document, EmbeddedDocument, StringField, ListField, EmbeddedDocumentField, DateTimeField
from datetime import datetime

class MedicalRecord(EmbeddedDocument):
    pass

class MedicalHistory(EmbeddedDocument):
    pass


class TraitmentPlantEmbedded(Document):
    pass


class PersonalInformation(Document):
    pass
