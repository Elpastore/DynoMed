from patient import Patient, MedicalRecord, VitalSigns, Medication, Surgery, Allergy
from datetime import datetime
from bson import ObjectId
from mongoengine import DoesNotExist, connect
import pymongo

connect('Record', host='mongodb://127.0.0.1:27017/Record')

# Example data for creating a patient

# delete all record
myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient['Record']
mycol = mydb['patient']
mycol.drop()

patient_data = {
    'full_name': 'John Doe',
    'birthday': datetime(1985, 5, 15),
    'gender': 'Male',
    'contact_information': '123-456-7890',
    'emergency_contact': 'Jane Doe, 123-456-7890',
    'medical_history': [
        MedicalRecord(
            chief_complaint='Headache',
            symptoms=['Headache', 'Nausea'],
            diagnoses=['Migraine'],
            vital_signs=VitalSigns(
                blood_pressure='120/80',
                heart_rate=72,
                temperature=98.6,
                respiration_rate=18
            ),
            medications=[
                Medication(
                    name='Ibuprofen',
                    dosage='200mg',
                    start_date=datetime(2024, 7, 1),
                    end_date=datetime(2024, 7, 10)
                )
            ],
            surgeries=[
                Surgery(
                    procedure='Appendectomy',
                    date=datetime(2010, 4, 20),
                    outcome='Successful'
                )
            ],
            allergies=[
                Allergy(
                    name='Penicillin',
                    reaction='Rash'
                )
            ]
        )
    ],
    'immunization_records': ['MMR', 'Tetanus'],
    'insurance_information': 'Insurance Company XYZ'
}

# Create and save the patient document
patient = Patient(**patient_data)
patient.save()

retrieved_patient = Patient.objects(full_name="John Doe").first()
print(f"Patient Name: {retrieved_patient.full_name}")
print(f"Date of Birth: {retrieved_patient.birthday}")
print(f"Gender: {retrieved_patient.gender}")
print(f"Contact Information: {retrieved_patient.contact_information}")
print(f"Emergency Contact: {retrieved_patient.emergency_contact}")
print(f"Chief Complaint: {retrieved_patient.medical_history[0].chief_complaint}")

# Print details of all prescribed medications
for medication in retrieved_patient.medical_history[0].medications:
    print(f"Medication Name: {medication.name}")
    print(f"Dosage: {medication.dosage}")
    print(f"Start Date: {medication.start_date}")
    print(f"End Date: {medication.end_date}")
    
print('Id of patient: ', patient.id)

new_id = "6689211c2df385fbeeab52a7"
try:
    # Find the patient by full name
    patient = Patient.objects.get(full_name="John Doe")

except DoesNotExist:
    print("Patient not found")
    patient = None

if patient:
    # Create a new medication record
    new_medication = Medication(
        name="Amoxicillin",
        dosage="500mg",
        start_date=datetime(2024, 7, 8),
        end_date=datetime(2024, 7, 15)
    )

    # Create a new medical record
    new_medical_record = MedicalRecord(
        chief_complaint="Severe cough and fever",
        symptoms=["cough", "fever", "sore throat"],
        diagnoses=["bronchitis"],
        vital_signs=VitalSigns(
            blood_pressure="120/80",
            heart_rate=80,
            temperature=38.5,
            respiration_rate=18
        ),
        medications=[new_medication],
        surgeries=[],
        allergies=[]
    )

    # Add the new medical record to the patient's medical history
    patient.medical_history.append(new_medical_record)
    # Save the updated patient document
    patient.save()
    original_patient = Patient.objects(pk=ObjectId(patient.id)).first()
    
    if original_patient:
        new_patient_id = ObjectId(new_id)
    new_patient_data = {
        'id': new_patient_id,
        'full_name': original_patient.full_name,
        'birthday': original_patient.birthday,
        'gender': original_patient.gender,
        'contact_information': original_patient.contact_information,
        'emergency_contact': original_patient.emergency_contact,
        'medical_history': original_patient.medical_history,
        'current_health_information': original_patient.current_health_information,
        'immunization_records': original_patient.immunization_records,
        'insurance_information': original_patient.insurance_information
    }

    new_patient = Patient(**new_patient_data)
    new_patient.save()

    # Step 3: Delete the original document
    original_patient.delete()
    print("New medical record with medication added successfully")