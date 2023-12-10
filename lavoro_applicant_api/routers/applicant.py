import uuid

from fastapi import APIRouter, status, HTTPException

from lavoro_applicant_api.helpers.applicant_helpers import create_applicant_profile
from lavoro_applicant_api.database.queries import (
    get_applicant_experiences,
    get_applicant_profile,
    update_applicant_profile,
    update_applicant_experience,
    delete_applicant_experience,
)

# from lavoro_library.models import (
#     CreateApplicantProfileRequest,
#     UpdateApplicantProfileRequest,
#     UpdateApplicantExperienceRequest,
# )

from lavoro_library.model.applicant_api.db_models import ApplicantProfile, Experience

from lavoro_library.model.applicant_api.dtos import (
    ApplicantProfileDTO,
    CreateApplicantProfileDTO,
    UpdateApplicantProfileDTO,
    UpdateApplicantExperienceDTO,
)

router = APIRouter(prefix="/applicant", tags=["applicant"])


@router.post("/create-applicant-profile/{account_id}", status_code=status.HTTP_201_CREATED)
def create_applicant(account_id: uuid.UUID, form_data: CreateApplicantProfileDTO):
    applicant_profile = get_applicant_profile(account_id)
    if applicant_profile:
        raise HTTPException(status_code=400, detail="Applicant profile already exists")
    result = create_applicant_profile(account_id, form_data)
    if not result:
        raise HTTPException(status_code=400, detail="Applicant profile could not be created")
    return {"detail": "Applicant profile created"}


@router.get("/get-applicant-profile/{account_id}")
def get_applicant(account_id: uuid.UUID):
    applicant_profile = get_applicant_profile(account_id)
    if not applicant_profile:
        raise HTTPException(status_code=404, detail="Applicant profile not found")
    return applicant_profile


@router.get("/get-experiences/{account_id}")
def get_experiences(account_id: uuid.UUID):
    experiences = get_applicant_experiences(account_id)
    if not experiences:
        raise HTTPException(status_code=404, detail="Applicant experiences not found")
    return experiences


@router.patch("/update-applicant-profile/{account_id}", status_code=status.HTTP_200_OK)
def update_applicant(account_id: uuid.UUID, form_data: UpdateApplicantProfileDTO):
    applicant_profile = get_applicant_profile(account_id)
    if not applicant_profile:
        raise HTTPException(status_code=404, detail="Applicant profile not found")
    result = update_applicant_profile(account_id, form_data)
    if not result:
        raise HTTPException(status_code=400, detail="Applicant profile could not be updated")
    return {"detail": "Applicant profile updated"}


@router.patch("/update-applicant-experience/{experience_id}", status_code=status.HTTP_200_OK)
def update_experience(experience_id: uuid.UUID, form_data: UpdateApplicantExperienceDTO):
    experience = get_applicant_experiences(experience_id)
    if not experience:
        raise HTTPException(status_code=404, detail="Applicant experience not found!")
    result = update_applicant_experience(experience_id, form_data)
    if not result:
        raise HTTPException(status_code=400, detail="Applicant experience could not be updated!")
    return {"detail": "Experience updated"}


@router.delete("/delete-applicant-experience/{experience_id}", status_code=status.HTTP_200_OK)
def delete_experience(experience_id: uuid.UUID):
    experience = get_applicant_experiences(experience_id)
    if not experience:
        raise HTTPException(status_code=404, detail="Applicant experience not found!")
    result = delete_applicant_experience(experience_id)
    if not result:
        raise HTTPException(status_code=400, detail="Applicant experience could not be deleted!")
    return {"detail": "Experience deleted"}
