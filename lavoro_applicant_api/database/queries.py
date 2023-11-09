from enum import Enum
from typing import List
import json
from uuid import UUID

from lavoro_applicant_api.database import db
from lavoro_library.models import ApplicantProfileDto, ApplicantProfile, Experience, ExperienceDto, Point


def create_applicant_profile(request: ApplicantProfileDto) -> ApplicantProfileDto:
    data = request.dict(exclude={'experiences'})
    values_tuple = tuple(convert_value(value) for value in data.values())

    sql = '''
        INSERT INTO applicant_profiles (first_name, last_name, education_level_id, age, gender, skills_id, account_id, cv_url, work_type_id, seniority_level, position_id, home_location, work_location_max_distance, contract_type_id, min_salary)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        '''

    result = db.execute_one((sql, values_tuple))

    if result and 'result' in result and result['result']:
        applicant_profile_id = result['result'][0]['id']
        data['id'] = applicant_profile_id
        print(f"ApplicantProfile inserted with ID: {applicant_profile_id}")
    else:
        print("Failed to insert ApplicantProfile.")
        applicant_profile_id = None

    if applicant_profile_id:
        applicant_profile_dto = ApplicantProfileDto(**data)
        experiences_data = request.experiences
        experiences_list = []

        for experience in experiences_data:
            experience_dict = experience.dict()
            experience_dict['applicant_profile_id'] = applicant_profile_id

            sql = '''
                    INSERT INTO experiences (company_name, position_id, years, applicant_profile_id)
                    VALUES (%s, %s, %s, %s) RETURNING id
                    '''

            values_tuple = tuple(convert_value(value) for value in experience_dict.values())
            result = db.execute_one((sql, values_tuple))

            experience_dict['id'] = result['result'][0]['id']
            experience_dto = ExperienceDto(**experience_dict)
            experiences_list.append(experience_dto)

        applicant_profile_dto.experiences = experiences_list
        return applicant_profile_dto
    else:
        print("Could not insert experiences without an applicant profile ID.")


def get_applicant_profiles() -> List[ApplicantProfileDto]:
    query_tuple = ("""
        SELECT 
            ap.id AS id,
            ap.first_name AS first_name,
            ap.last_name AS last_name,
            ap.education_level_id AS education_level_id,
            ap.age AS age,
            ap.gender AS gender,
            ap.skills_id AS skills_id,
            ap.account_id AS account_id,
            ap.cv_url AS cv_url,
            ap.work_type_id AS work_type_id,
            ap.seniority_level AS seniority_level,
            ap.position_id AS position_id,
            ap.home_location AS home_location,
            ap.work_location_max_distance AS work_location_max_distance,
            ap.contract_type_id AS contract_type_id,
            ap.min_salary AS min_salary,
            exp.id AS experience_id,
            exp.company_name AS experience_company_name,
            exp.position_id AS experience_position_id,
            exp.years AS experience_years,
            exp.applicant_profile_id AS experience_applicant_profile_id
        FROM 
            applicant_profiles ap
        LEFT JOIN experiences exp
            ON ap.id = exp.applicant_profile_id;
                   """, None)

    result = db.execute_one(query_tuple)

    applicants = {}

    for row in result['result']:
        applicant_id = row['id']

        # Initialize the applicant profile if it's not already in the dictionary
        if applicant_id not in applicants:
            applicant_data = {
                'id': row['id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'education_level_id': row['education_level_id'],
                'age': row['age'],
                'gender': row['gender'],
                'skills_id': row['skills_id'],
                'account_id': row['account_id'],
                'cv_url': row['cv_url'],
                'home_location': row['home_location'],
                'work_type_id': row['work_type_id'],
                'seniority_level': row['seniority_level'],
                'position_id': row['position_id'],
                'work_location_max_distance': row['work_location_max_distance'],
                'contract_type_id': row['contract_type_id'],
                'min_salary': row['min_salary'],
                'experiences': []
            }
            applicants[applicant_id] = ApplicantProfileDto(**applicant_data)

        # Add experience to the applicant profile if it exists
        if row['experience_id']:
            experience_data = {
                'id': row['experience_id'],
                'company_name': row['experience_company_name'],
                'position_id': row['experience_position_id'],
                'years': row['experience_years']
            }
            applicants[applicant_id].experiences.append(ExperienceDto(**experience_data))

    # Convert dictionary to list and return it
    return list(applicants.values())


def convert_value(value):
    if isinstance(value, UUID):
        return str(value)
    elif isinstance(value, Enum):
        return value.value
    elif isinstance(value, dict):
        if 'x' in value and 'y' in value:
            return f"({value['x']}, {value['y']})"
        else:
            return json.dumps(value)
    else:
        return value
