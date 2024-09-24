#!/usr/bin/python3
"""test all methods in med_pract"""
from datetime import datetime
from dyno_med import Medical, Expert
from werkzeug.datastructures import FileStorage
import io

# dummy picture file
picture_data = io.BytesIO(b"dummy image content")
picture_file = FileStorage(picture_data, filename="profile.jpg", content_type="image/jpeg")

# dummy certificate file
certificate_data_1 = io.BytesIO(b"dummy certificate content 1")
certificate_file_1 = FileStorage(certificate_data_1, filename="certificate1.pdf", content_type="application/pdf")

certificate_data_2 = io.BytesIO(b"dummy certificate content 2")
certificate_file_2 = FileStorage(certificate_data_2, filename="certificate2.jpg", content_type="image/jpeg")


# create an example user profile dictionary
profile_data = {
    'fullName': 'John Doe',
    'professional_title': 'Cardiologist',
    'bio_data': 'An experienced cardiologist with over 15 years of practice.',
    'gender': 'male',
    'dateOfBirth': '10-12-1975',
    'location': '123 Main St, Springfield, IL, USA',
}

# Retrieve the expert document (create one if does not exist)
med_user = Expert.objects(email="test1@gmail.com").first()
print(f"id: {med_user.id}")

# initialize medical instances and update profile:
medical = Medical()
medical.update_med_user_profile(med_user=med_user, profile_data=profile_data, file=picture_file)


# certification form data
cert_data = {
    'certificationName[]': ['Certification in Advanced Cardiology', 'Certification in Emergency Care']
}
print(cert_data.get('certificationName[]')[0])

# Create a list of files to simulate multiple certification file uploads
files = [certificate_file_1, certificate_file_2]

# Test the update_med_user_certifications method
try:
    medical.update_med_user_certifications(med_user=med_user, cert_data=cert_data, files=files)
    print("Certifications updated successfully!")
except Exception as e:
    print(f"An error occurred while updating certifications: {e}")

# Experience data example
experience_data = {
    'company': ['HealthTech', 'MediCorp'],
    'role': ['Cardiologist', 'Chief Medical Officer'],
    'startDate': ['01-10-2010', '05-02-2020'],
    'endDate': ['12-15-2015', 'Present'],
    'responsibilities': [
        'Perform cardiovascular surgeries and patient care.',
        'Oversee hospital operations and manage medical staff.'
    ]
}
# initialize the medical instances and update experience
medical.update_med_user_experience(med_user=med_user, experience_data=experience_data)

# Education data example
education_data = {
    'university': ['Harvard Medical School'],
    'course': ['Cardiology'],
    'entryYear': ['2002'],
    'endYear': ['2006'],
    'degree': ['Doctor of Medicine (MD)']
}
# Initialize Medical instance and update education
medical.update_med_user_education(med_user=med_user, education_data=education_data)

# Address data example
address_data = {
    'country_of_origin': 'USA',
    'state_of_origin': 'Illinois',
    'local_government_area': 'Springfield',
    'town_of_origin': 'Springfield'
}
medical.update_med_user_address(med_user=med_user, address_data=address_data)

# Next of Kin data example
kin_data = {
    'KinName': 'Jane Doe',
    'relationship': 'Spouse',
    'email': 'janedoe@example.com',
    'number': '+1 312-555-1234',
    'address': '456 Oak St, Springfield, IL, USA'
}
medical.update_med_user_kin(med_user=med_user, kin_data=kin_data)

