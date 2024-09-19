from datetime import datetime
from werkzeug.utils import secure_filename
from typing import List, Dict, Any, Optional
# from dyno_med import *
from bson import ObjectId
import os
import re

class Medical:
    def __init__(self, med_user: Optional[Any] = None, data: Optional[Dict[str, Any]] = None,
                 files: Optional[Dict[str, Any]] = None):
        self.UPLOAD_FOLDER: str = '/home/pc/DynoMed/dyno_med/file_DataBase/certificate'
        self.UPLOAD_PIC: str = '/home/pc/DynoMed/dyno_med/file_DataBase/Picture'
        self.ALLOWED_EXTENSIONS: List[str] = ['jpg', 'jpeg', 'png']

        self.profile_picture: Optional[str] = None
        self.username: Optional[str] = None
        self.first_name: Optional[str] = None
        self.middle_name: Optional[str] = None
        self.last_name: Optional[str] = None
        self.age: Optional[int] = None
        self.gender: Optional[str] = None
        self.date_of_birth: Optional[datetime] = None
        self.country_of_origin: Optional[str] = None
        self.state_of_origin: Optional[str] = None
        self.local_government_area: Optional[str] = None
        self.town_of_origin: Optional[str] = None
        self.email: Optional[str] = None
        self.mobile_num: Optional[int] = None
        self.linkedin: Optional[str] = None
        self.password: Optional[str] = None
        self.residential_address: Dict[str, str] = {}
        self.next_of_kin: Dict[str, str] = {}
        self.education: List[Dict[str, str]] = []
        self.certificates: List[Dict[str, str]] = []

    def is_valid_email(self, email: str) -> bool:
        if not email:
            return False
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return email_regex.match(email) is not None

    def allowed_file(self, filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    

    def _check_input_params(self, med_user: object, data: Dict[str, Any],
                            files: Optional[Dict[str, Any]] = None,
                            user_id: Optional[Any] = None):
        """
        check for edge cases for ech of the prameters

        Args:
            med_user: An instance of mongodb document object
            data: A dictionary from the web form containg the user data
            file: The file format (optional)
            user_id: The document id of the user(optional)
        """
        if not med_user:
            raise ValueError('No user found, please provide medical user')
        if not data:
            raise ValueError('No form data found, please provide the object from the database')
    
    def _ensure_string(self, value: Any) -> str:
        """ convert the value to a string if a value is provided"""
        if value is None:
            return ""
        return str(value)

    def _ensure_date(self, value: Any) -> datetime:
        """
        convert the value to a datetime format if a value is provided and is not a datetime
        """
        if isinstance(value, datetime):
            return value
        if not value:
            return None
        try:
            return datetime.strptime(value, '%m-%d-%Y')
        except ValueError:
            return None

    def _handle_fullName(self, fullname: str) -> List[str]:
        """
        Extract the first name, middle name and last name from the full name
        """
        name_segments = self._ensure_string(fullname).split()
        if len(name_segments) == 0:
            return ['', '', '']
        elif len(name_segments) == 1:
            return [name_segments[0], '', '']
        elif len(name_segments) == 2:
            return [name_segments[0], '', name_segments[1]]
        else:
            return [name_segments[0], ' '.join(name_segments[1:-1]), name_segments[-1]]

    def _handle_address(self, address: str) -> List[str]:
        """
        Extract the street, city, state, and country from thr address
        """
        address_parts = self._ensure_string(address).split(',')
        address_parts = [part.strip() for part in address_parts]
        while len(address_parts) < 4:
            address_parts.append('')
        return address_parts[:4]

    def _handle_num(self, number: Any) -> List[int]:
        """
        extract the country code and the telephone number from the number
        """
        if not number:
            return []

        number_split = number.split()
        if len(number_split[1]) == 10:
            return f"{number_split[0]}{''}{number_split[1]}"
        else:
            return ''

    def update_med_user_experience(self, med_user: object, experience_data: Dict[str, Any],
                                   file: Optional[Dict[str, Any]] = None, user_id: Optional[str] = None):
        """
        update the user using the experience form of the user

        Args:
            med_user: The user document object from th database
            experience_data: dictionary from the user form containg the experience data
        """
        from dyno_med import Experience
        self._check_input_params(med_user, experience_data)
        try:
            new_experience = []
            for index in range(len(experience_data.get('company', []))):
                experience = Experience(
                    company=self._ensure_string(experience_data['company'][index]),
                    role=self._ensure_string(experience_data['role'][index]),
                    start_date=self._ensure_date(experience_data['startDate'][index]),
                    end_date=self._ensure_date(experience_data['endDate'][index]),
                    responsibilities=self._ensure_string(experience_data['responsibilities'][index])
                )
                new_experience.append(experience)
            med_user.experience = new_experience
            med_user.save()
        except Exception as e:
            raise Exception(f"Failed to update experience: {str(e)}")

    def update_med_user_profile(self, med_user: object, profile_data: Dict[str, Any], file:
                                Optional[Dict[str, Any]] = None, user_id: Optional[str] = None):
        """
        update the user database data using the  profile form of the user

        Args:
            med_user: The user document object from the database
            profile_data: dictionary from the user form containg the profile data
            file: The user picture
        """
        from dyno_med import ResidentialAddress
        if not file:
            raise ValueError(" please provide the picture file of the user")
        
        self._check_input_params(med_user, profile_data)
        street, city, state, country = self._handle_address(self._ensure_string
                                                            (profile_data.get('location', '')))
        try:
            # Handle file upload
            if file and self.allowed_file(file.filename):
                secure_name = secure_filename(file.filename)
                file_path = os.path.join(self.UPLOAD_PIC, secure_name)
                file.save(file_path)
                med_user.profile_picture = file_path
                print(f"picture path: {file_path}")
            
            # update the present location of the user
            location = ResidentialAddress(
                country=self._ensure_string(country),
                state= self._ensure_string(state),
                city=self._ensure_string(city),
                street=self._ensure_string(street),
            )
            first_name, middle_name, last_name = self._handle_fullName(profile_data.get('fullName', ''))
            med_user.first_name = first_name
            med_user.middle_name = middle_name
            med_user.last_name = last_name
            med_user.professional_title = self._ensure_string(profile_data.get('professional_title', ''))
            med_user.bio_data = self._ensure_string(profile_data.get('bio_data', ''))
            med_user.gender = self._ensure_string(profile_data.get('gender', ''))
            med_user.date_of_birth = self._ensure_date(profile_data.get('dateOfBirth', ''))

            med_user.residential_address = location
            med_user.save()
        except Exception as e:
            raise Exception(f"Failed to update profile: {str(e)}")

    def update_med_user_education(self, med_user: object, education_data: Dict[str, Any]):
        """
        update the user database data using the Educatio form of the user

        Args:
            med_user: The user document object from the database
            profile_data: dictionary from the user form containg the Education data
        """
        from dyno_med import Education
        self._check_input_params(med_user, education_data)
        try:
            new_education = []
            for index in range(len(education_data.get('university', []))):
                education = Education(
                    university=self._ensure_string(education_data['university'][index]),
                    course=self._ensure_string(education_data['course'][index]),
                    entry_yr=self._ensure_string(education_data['entryYear'][index]),
                    completion_yr=self._ensure_string(education_data['endYear'][index]),
                    degree=self._ensure_string(education_data['degree'][index])
                )
                new_education.append(education)
            med_user.education = new_education
            med_user.save()
        except Exception as e:
            raise Exception(f"Failed to update education: {str(e)}")
        
    def update_med_user_certifications(self, med_user: object, cert_data: Dict[str, Any], files):
        """
        update the certificate of the user in the databse from the certificate data form

        Args:
            med_user: User document object to update in the database.
            cert_data: Certification data from the form.
            files: List of files uploaded for certificates.
        """
        from dyno_med import Certificate

        self._check_input_params(med_user, cert_data)
        
        new_certifications = []

        for idx, file in enumerate(files):
            cert_name_key = cert_data.get('certificationName[]')[0]
            if cert_name_key and file and self.allowed_file(file.filename):
                print(f"the if statenment: {cert_name_key}")
                try:
                    # Secure file name
                    secure_filename_value = secure_filename(file.filename)
                    file_path = os.path.join(self.UPLOAD_FOLDER, secure_filename_value)
                    file.save(file_path)

                    # Create a certificate object
                    certificate = Certificate(
                        certificate_name=self._ensure_string(cert_name_key),
                        certificate_file_path=file_path
                    )
                    new_certifications.append(certificate)
                except Exception as e:
                    raise Exception(f"Unable to update certification data in the database: {e}")

        if new_certifications:
            med_user.certificates = new_certifications
            med_user.save()

    def update_med_user_address(self, med_user: object, address_data: Dict[str, Any]):
        self._check_input_params(med_user, address_data)
        """
        update the address of the user in the databse from the adress data form

        Args:
            med_user: user document object to update in the database
            address_data: the user adress dict containing the data
        """
        try:
            med_user.country_of_origin = self._ensure_string(address_data.get('country_of_origin', ''))
            med_user.state_of_origin = self._ensure_string(address_data.get('state_of_origin', ''))
            med_user.local_government_area = self._ensure_string(address_data.get('local_government_area', ''))
            med_user.town_of_origin = self._ensure_string(address_data.get('town_of_origin', ''))
            med_user.save()
        except Exception as e:
            raise Exception(f"Failed to update address: {str(e)}")

    def update_med_user_kin(self, med_user: object, kin_data: Dict[str, Any]):
        self._check_input_params(med_user, kin_data)
        """
        update the next of kin data of the user in the databse from the next_of_kin data form

        Args:
            med_user: user document object to update in the database
            kin_data: the next_of_kin dict containing the data
        """
        from dyno_med import NextOfKin
        try:
            first_name, middle_name, last_name = self._handle_fullName(kin_data.get('KinName', ''))
            street, city, state, country = self._handle_address(kin_data.get('address', ''))
            next_of_kin = NextOfKin(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                relationship=self._ensure_string(kin_data.get('relationship', '')),
                residential_address_email=self._ensure_string(kin_data.get('email', '')),
                residential_address_telephone_num=kin_data.get('number', ''),
                residential_address_country=country,
                residential_address_state=state, 
                residential_address_city=city,
                residential_address_street=street
            )
            med_user.next_of_kin = next_of_kin
            med_user.save()
        except Exception as e:
            raise Exception(f"Failed to update next of kin: {str(e)}")

    
    def retrieve_med_user(self, med_user: object) -> dict:
        """Retrieve the user data from the database"""
        # Retrieve the full name:
        fullName = ' '.join(filter(None, [
            getattr(med_user, 'first_name', ''),
            getattr(med_user, 'middle_name', ''),
            getattr(med_user, 'last_name', '')
        ]))

        # Retrieve the location of the user
        location = ' '.join(filter(None, [
            getattr(med_user.residential_address, 'street', ''),
            getattr(med_user.residential_address, 'city', ''),
            getattr(med_user.residential_address, 'state', ''),
            getattr(med_user.residential_address, 'country', '')
        ]))

        # Retrieve the education
        education = []
        if hasattr(med_user, 'education'):
            for edu in med_user.education:
                education.append({
                    'university': getattr(edu, 'university', ''),
                    'course': getattr(edu, 'course', ''),
                    'entry_yr': getattr(edu, 'entry_yr', ''),
                    'completion_yr': getattr(edu, 'completion_yr', ''),
                    'degree': getattr(edu, 'degree', '')
                })
        
        # Retrieve experience from the database
        experience = []
        if hasattr(med_user, 'experience'):
            for exp in med_user.experience:
                experience.append({
                    'company': getattr(exp, 'company', ''),
                    'role': getattr(exp, 'role', ''),
                    'start_date': getattr(exp, 'start_date', ''),
                    'end_date': getattr(exp, 'end_date', ''),
                    'responsibilities': getattr(exp, 'responsibilities', '')
                })

        # Retrieve the med_user certificate
        certificates = []
        if hasattr(med_user, 'certificates'):
            for cert in med_user.certificates:
                certificates.append({
                    'certificate_name': getattr(cert, 'certificate_name', ''),
                    'certificate_file_path': getattr(cert, 'certificate_file_path', '')
                })

        # Retrieve the next of kin data from the database
        kin_full_name = ' '.join(filter(None, [
            getattr(med_user.next_of_kin, 'first_name', ''),
            getattr(med_user.next_of_kin, 'middle_name', ''),
            getattr(med_user.next_of_kin, 'last_name', '')
        ]))
        
        address = ' '.join(filter(None, [
            getattr(med_user.next_of_kin, 'residential_address_street', ''),
            getattr(med_user.next_of_kin, 'residential_address_city', ''),
            getattr(med_user.next_of_kin, 'residential_address_state', ''),
            getattr(med_user.next_of_kin, 'residential_address_country', '')
        ]))
        
        kin = {
            'fullName': kin_full_name,
            'address': address,
            'relationship': getattr(med_user.next_of_kin, 'relationship', ''),
            'email': getattr(med_user.next_of_kin, 'residential_address_email', ''),
        }
        
        med_user_data = {
            'profile_picture': getattr(med_user, 'profile_picture', ''),
            'email': getattr(med_user, 'email', ''),
            'username': getattr(med_user, 'username', ''),
            'fullName': fullName,
            'professional_title': getattr(med_user, 'professional_title', ''),
            'gender': getattr(med_user, 'gender', ''),
            'bio_data': getattr(med_user, 'bio_data', ''),
            'location': location,
            'experience': experience,
            'education': education,
            'certificates': certificates,
            'date_of_birth': getattr(med_user, 'date_of_birth', ''),
            'country_of_origin': getattr(med_user, 'country_of_origin', ''),
            'state_of_origin': getattr(med_user, 'state_of_origin', ''),
            'local_government_area': getattr(med_user, 'local_government_area', ''),
            'town_of_origin': getattr(med_user, 'town_of_origin', ''),
            'kin': kin
        }
        
        return med_user_data