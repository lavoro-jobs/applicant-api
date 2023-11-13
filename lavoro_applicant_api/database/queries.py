from enum import Enum
import json
from uuid import UUID

from lavoro_applicant_api.database import db
from lavoro_library.models import ApplicantProfileDto, ApplicantProfile, Experience, ExperienceDto, Point

from lavoro_applicant_api.database.sql_queries import INSERT_APPLICANT_PROFILE_SQL, INSERT_EXPERIENCE_SQL

def create_applicant_profile(request: ApplicantProfileDto) -> ApplicantProfileDto:
    applicant_profile_id = insert_applicant_profile(request)
    insert_experiences(request.experiences, applicant_profile_id)
    return

def insert_applicant_profile(request: ApplicantProfileDto):
    data = request.dict(exclude={'experiences'})
    values_tuple = tuple(convert_value(value) for value in data.values())
    result = execute_query(INSERT_APPLICANT_PROFILE_SQL, values_tuple)
    return extract_id(result)

def insert_experiences(experiences_data, applicant_profile_id):
    for experience in experiences_data:
        experience_dict = experience.dict()
        experience_dict['applicant_profile_id'] = applicant_profile_id
        values_tuple = tuple(convert_value(value) for value in experience_dict.values())
        execute_query(INSERT_EXPERIENCE_SQL, values_tuple)
    return

def execute_query(sql, values_tuple):
    return db.execute_one((sql, values_tuple))

def extract_id(result):
    return result['result'][0]['id'] if result and 'result' in result else None


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
