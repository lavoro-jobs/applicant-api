import uuid

from fastapi import APIRouter, status, HTTPException

from lavoro_applicant_api.helpers.applicant_helpers import create_applicant_profile
from lavoro_applicant_api.database.queries import get_applicant_experiences, get_applicant_profile, \
    update_applicant_profile, update_applicant_experience, get_applicant_experience

from lavoro_library.models import CreateApplicantProfileRequest, UpdateApplicantProfileRequest, UpdateApplicantExperienceRequest

router = APIRouter(prefix="/applicant", tags=["applicant"])


@router.post("/create-applicant-profile/{account_id}", status_code=status.HTTP_201_CREATED)
def create_applicant(account_id: uuid.UUID, form_data: CreateApplicantProfileRequest):
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
    experiences = get_applicant_experiences(applicant_profile.account_id)
    applicant_profile.experiences = experiences
    if not applicant_profile:
        raise HTTPException(status_code=404, detail="Applicant profile not found")
    return applicant_profile


@router.patch("/update-applicant-profile/{account_id}", status_code=status.HTTP_200_OK)
def update_applicant(account_id: uuid.UUID, form_data: UpdateApplicantProfileRequest):
    applicant_profile = get_applicant_profile(account_id)
    if not applicant_profile:
        raise HTTPException(status_code=404, detail="Applicant profile not found")
    result = update_applicant_profile(account_id, form_data)
    if not result:
        raise HTTPException(status_code=400, detail="Applicant profile could not be updated")
    return {"detail": "Applicant profile updated"}


@router.patch("/update-applicant-experience/{experience_id}", status_code=status.HTTP_200_OK)
def update_experience(experience_id: uuid.UUID, form_data: UpdateApplicantExperienceRequest):
    experience = get_applicant_experience(experience_id)
    if not experience:
        raise HTTPException(status_code=404, detail="Applicant experience not found!")
    result = update_applicant_experience(experience_id, form_data)
    if not result:
        raise HTTPException(status_code=400, detail="Applicant experience could be updated!")
    return {"detail": "Experience updated"}
