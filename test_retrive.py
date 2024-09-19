#!/usr/bin/python3
"""test retrieve_med_user method"""

from dyno_med import Medical, Expert
import json

# Retrieve the expert document (assuming it already exists)
med_user = Expert.objects(username="Wizy").first()
print(f"id: {med_user.id}")

# Initialize Medical instance
medical = Medical()

# Use the retrieve_med_user method to get the user's data
retrieved_data = medical.retrieve_med_user(med_user)

# Print the retrieved data
print("Retrieved Medical User Data:")
print(json.dumps(retrieved_data, indent=2, default=str))

# You can also access specific parts of the data if needed
print("\nSpecific Data Points:")
print(f"Full Name: {retrieved_data['fullName']}")
print(f"Professional Title: {retrieved_data['professional_title']}")
print(f"Location: {retrieved_data['location']}")

# Print education details
print("\nEducation:")
for edu in retrieved_data['education']:
    print(f"- {edu['degree']} in {edu['course']} from {edu['university']} ({edu['entry_yr']} - {edu['completion_yr']})")

# Print experience details
print("\nExperience:")
for exp in retrieved_data['experience']:
    print(f"- {exp['role']} at {exp['company']} ({exp['start_date']} - {exp['end_date']})")
    print(f"  Responsibilities: {exp['responsibilities']}")

# Print certificates
print("\nCertificates:")
for cert in retrieved_data['certificates']:
    print(f"- {cert['certificate_name']}")

# Print next of kin details
print("\nNext of Kin:")
print(f"Name: {retrieved_data['kin']['fullName']}")
print(f"Relationship: {retrieved_data['kin']['relationship']}")
print(f"Contact: {retrieved_data['kin']['email']}")
