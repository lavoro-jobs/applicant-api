import uuid

from fastapi import APIRouter, status, HTTPException

from lavoro_applicant_api.helpers.applicant_helpers import create_applicant_profile
from lavoro_applicant_api.database.queries import get_applicant_profile

from lavoro_library.models import CreateApplicantProfileRequest

router = APIRouter(prefix="/applicant", tags=["applicant"])


@router.post("/create_applicant_profile/{account_id}", status_code=status.HTTP_201_CREATED)
def create_applicant(account_id: uuid.UUID, form_data: CreateApplicantProfileRequest):
    applicant_profile = get_applicant_profile(account_id)
    if applicant_profile:
        raise HTTPException(status_code=400, detail="Applicant profile already exists")
    applicant_id = create_applicant_profile(account_id, form_data)
    if not applicant_id:
        raise HTTPException(status_code=400, detail="Applicant profile could not be created")
    return {"detail": "Applicant profile created"}
