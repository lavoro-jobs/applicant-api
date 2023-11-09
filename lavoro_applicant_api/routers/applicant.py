from fastapi import APIRouter

from typing import List

from lavoro_applicant_api.database.queries import (
    get_applicant_profiles,
    create_applicant_profile,
)

from lavoro_library.models import (
    ApplicantProfileDto,
    CreateApplicantProfileRequest
)


router = APIRouter(prefix="/applicant", tags=["applicant"])


@router.get("/get_applicant_profiles", response_model=List[ApplicantProfileDto])
def get_applicants():
    result = get_applicant_profiles()
    return result


@router.post("/create_applicant_profile", response_model=ApplicantProfileDto)
def create_applicant(request: CreateApplicantProfileRequest):
    result = create_applicant_profile(request)
    return result