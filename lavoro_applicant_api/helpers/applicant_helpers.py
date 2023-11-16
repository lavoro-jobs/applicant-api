from lavoro_applicant_api.database.queries import insert_applicant_profile, insert_experiences
from lavoro_library.models import CreateApplicantProfileRequest


def create_applicant_profile(account_id, form_data: CreateApplicantProfileRequest):
    applicant_info = form_data.model_dump(exclude={"experiences"})
    experiences = form_data.experiences
    applicant_profile_id = insert_applicant_profile(account_id, **applicant_info)
    insert_experiences(experiences, applicant_profile_id)
    return applicant_profile_id
