from enum import Enum
import json
from uuid import UUID

from lavoro_applicant_api.database import db
from lavoro_library.models import ApplicantProfileDto, CreateApplicantProfileRequest, ApplicantProfile, Experience, \
    ExperienceDto, Point


INSERT_APPLICANT_PROFILE_SQL = '''
    INSERT INTO applicant_profiles (
        first_name, last_name, education_level_id, age, gender, skills_id, 
        account_id, cv_url, work_type_id, seniority_level, position_id, 
        home_location, work_location_max_distance, contract_type_id, min_salary
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
'''


INSERT_EXPERIENCE_SQL = '''
    INSERT INTO experiences (company_name, position_id, years, applicant_profile_id)
    VALUES (%s, %s, %s, %s) RETURNING id
'''


def create_applicant_profile(form_data: CreateApplicantProfileRequest):
    applicant_profile_id = insert_applicant_profile(form_data)
    insert_experiences(form_data.experiences, applicant_profile_id)
    return


def insert_applicant_profile(form_data: CreateApplicantProfileRequest):
    query_tuple = prepare_applicant_profile_data(form_data)
    result = db.execute_one(query_tuple)
    return extract_id(result)


def insert_experiences(experiences, applicant_profile_id):
    query_tuples = [prepare_experience_data(experience, applicant_profile_id) for experience in experiences]
    db.execute_many(query_tuples)


def prepare_applicant_profile_data(form_data: CreateApplicantProfileRequest):
    return (
        INSERT_APPLICANT_PROFILE_SQL,
        (
            form_data.first_name, form_data.last_name,
            form_data.education_level_id, form_data.age, convert_value(form_data.gender),
            form_data.skills_id, convert_value(form_data.account_id), form_data.cv_url,
            form_data.work_type_id, form_data.seniority_level,
            form_data.position_id, convert_value(form_data.home_location),
            form_data.work_location_max_distance, form_data.contract_type_id,
            form_data.min_salary
         )
    )


def prepare_experience_data(experience, applicant_profile_id):
    return (
        INSERT_EXPERIENCE_SQL,
        (
            experience.company_name,
            experience.position_id,
            experience.years,
            applicant_profile_id
        )
    )


def extract_id(result):
    return result["result"][0]["id"] if result["result"] else None


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
