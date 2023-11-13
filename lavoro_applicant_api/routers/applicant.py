from typing import List

from fastapi import APIRouter, status

from lavoro_applicant_api.database.queries import (
    create_applicant_profile,
)

from lavoro_library.models import (
    CreateApplicantProfileRequest
)

router = APIRouter(prefix="/applicant", tags=["applicant"])

@router.post("/create_applicant_profile", status_code=status.HTTP_201_CREATED)
def create_applicant(form_data: CreateApplicantProfileRequest):
    create_applicant_profile(form_data)
    return
