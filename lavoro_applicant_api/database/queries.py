from lavoro_applicant_api.database import db
from lavoro_library.models import ApplicantProfileDto, CreateApplicantProfileRequest, ApplicantProfile, Experience, \
    ExperienceDto, Point
from lavoro_applicant_api.helpers.data_helpers import prepare_applicant_profile_data, prepare_experience_data, extract_id


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


