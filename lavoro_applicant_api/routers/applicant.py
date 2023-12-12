import uuid
from typing import List

from fastapi import APIRouter, status

from lavoro_applicant_api.services import applicant_service
from lavoro_library.model.applicant_api.dtos import (
    CreateApplicantProfileDTO,
    CreateExperienceDTO,
    UpdateApplicantProfileDTO,
    UpdateApplicantExperienceDTO,
)

router = APIRouter(prefix="/applicant", tags=["applicant"])


@router.post("/create-applicant-profile/{account_id}", status_code=status.HTTP_201_CREATED)
def create_applicant(account_id: uuid.UUID, form_data: CreateApplicantProfileDTO):
    return applicant_service.create_applicant_profile(account_id, form_data)


@router.post("/create-experiences/{account_id}", status_code=status.HTTP_201_CREATED)
def create_experiences(account_id: uuid.UUID, form_data: List[CreateExperienceDTO]):
    return applicant_service.create_experiences(account_id, form_data)


@router.get("/get-applicant-profile/{account_id}")
def get_applicant(account_id: uuid.UUID):
    return applicant_service.get_applicant_profile(account_id)


@router.get("/get-experiences/{account_id}")
def get_experiences(account_id: uuid.UUID):
    return applicant_service.get_experiences(account_id)


@router.patch("/update-applicant-profile/{account_id}", status_code=status.HTTP_200_OK)
def update_applicant(account_id: uuid.UUID, form_data: UpdateApplicantProfileDTO):
    return applicant_service.update_applicant_profile(account_id, form_data)


@router.patch("/update-applicant-experience/{experience_id}", status_code=status.HTTP_200_OK)
def update_experience(experience_id: uuid.UUID, form_data: UpdateApplicantExperienceDTO):
    return applicant_service.update_experience(experience_id, form_data)


@router.delete("/delete-applicant-experience/{experience_id}", status_code=status.HTTP_200_OK)
def delete_experience(experience_id: uuid.UUID):
    return applicant_service.delete_experience(experience_id)
