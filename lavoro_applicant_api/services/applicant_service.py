import uuid

from fastapi import HTTPException

from lavoro_applicant_api.database import queries
from lavoro_library.model.applicant_api.dtos import CreateApplicantProfileDTO, UpdateApplicantProfileDTO


def get_applicant_profile(account_id: uuid.UUID):
    applicant_profile = queries.get_applicant_profile(account_id)
    if not applicant_profile:
        raise HTTPException(status_code=404, detail="Applicant profile not found")
    return applicant_profile


def create_applicant_profile(account_id: uuid.UUID, form_data: CreateApplicantProfileDTO):
    applicant_profile = form_data.model_dump(exclude={"experiences"})
    result = queries.create_applicant_profile(account_id, **applicant_profile)
    if not result:
        raise HTTPException(status_code=400, detail="Applicant profile could not be created")
    if form_data.experiences:
        result = queries.create_experiences(account_id, form_data.experiences)
        if not result:
            raise HTTPException(status_code=400, detail="Applicant experiences could not be created")
    return result


def get_experiences(account_id: uuid.UUID):
    experiences = queries.get_applicant_experiences(account_id)
    if not experiences:
        raise HTTPException(status_code=404, detail="Applicant experiences not found")
    return experiences


def update_applicant_profile(account_id: uuid.UUID, form_data: UpdateApplicantProfileDTO):
    result = queries.update_applicant_profile(account_id, form_data)
    if not result:
        raise HTTPException(status_code=400, detail="Applicant profile could not be updated")
    return result


def update_experience(experience_id: uuid.UUID, form_data: UpdateApplicantProfileDTO):
    result = queries.update_experience(experience_id, form_data)
    if not result:
        raise HTTPException(status_code=400, detail="Experience could not be updated")
    return result


def delete_experience(experience_id: uuid.UUID):
    result = queries.delete_applicant_experience(experience_id)
    if not result:
        raise HTTPException(status_code=400, detail="Experience could not be deleted")
    return result
