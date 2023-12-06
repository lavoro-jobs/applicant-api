from lavoro_applicant_api.database.queries import (
    insert_applicant_profile,
    insert_experiences,
)

# from lavoro_library.models import CreateApplicantProfileRequest
from lavoro_library.model.applicant_api.dtos import CreateApplicantProfileDTO


def create_applicant_profile(account_id, form_data: CreateApplicantProfileDTO):
    applicant_info = form_data.model_dump(exclude={"experiences"})
    experiences = form_data.experiences
    created_applicant_profile = insert_applicant_profile(account_id, **applicant_info)
    created_experiences = insert_experiences(experiences, created_applicant_profile.account_id)
    return created_applicant_profile
