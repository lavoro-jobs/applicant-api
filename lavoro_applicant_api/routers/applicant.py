from fastapi import APIRouter

from typing import List

from lavoro_applicant_api.database.queries import (
    get_applicant_profiles,
)

from lavoro_library.models import (
    ApplicantProfileResponse,
)


router = APIRouter(prefix="/applicant", tags=["applicant"])


@router.get("/get_applicant_profiles", response_model=List[ApplicantProfileResponse])
def get_applicants():
    result = get_applicant_profiles()
    return result

