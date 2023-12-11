import base64
import uuid
from typing import List, Union

from lavoro_applicant_api.database import db
from lavoro_library.models import (
    ApplicantProfileInDB,
    CreateExperienceRequest,
    Gender,
    Experience,
    Point,
    UpdateApplicantProfileRequest,
    UpdateApplicantExperienceRequest,
    ExperienceInDB,
)


def get_applicant_profile(account_id: uuid.UUID):
    query_tuple = (
        "SELECT * FROM applicant_profiles WHERE account_id = %s",
        (account_id,),
    )
    result = db.execute_one(query_tuple)
    if result["result"]:
        applicant_profile_in_db = ApplicantProfileInDB(**result["result"][0])
        applicant_profile_in_db.cv = base64.b64encode(applicant_profile_in_db.cv).decode("utf-8")
        return applicant_profile_in_db
    else:
        return None


def get_applicant_experiences(account_id: uuid.UUID):
    query_tuple = (
        "SELECT * FROM experiences WHERE applicant_account_id = %s",
        (account_id,),
    )
    result = db.execute_one(query_tuple)
    if result["result"]:
        return [Experience(**experience) for experience in result["result"]]
    else:
        return []


def get_applicant_experience(experience_id: uuid.UUID):
    query_tuple = ("SELECT * FROM experiences WHERE id = %s", (experience_id,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return [Experience(**experience) for experience in result["result"]]
    else:
        return []


def update_applicant_profile(account_id: uuid.UUID, form_data: UpdateApplicantProfileRequest):
    prepare_tuple = prepare_fields(account_id, form_data)
    update_fields = prepare_tuple[0]
    query_params = prepare_tuple[1]

    query = f"UPDATE applicant_profiles SET {', '.join(update_fields)} WHERE account_id = %s RETURNING *"
    result = db.execute_one((query, tuple(query_params)))

    if result["result"]:
        applicant_profile_in_db = ApplicantProfileInDB(**result["result"][0])
        applicant_profile_in_db.cv = base64.b64encode(applicant_profile_in_db.cv).decode("utf-8")
        return applicant_profile_in_db
    return None


def update_applicant_experience(experience_id: uuid.UUID, form_data: UpdateApplicantExperienceRequest):
    prepare_tuple = prepare_fields(experience_id, form_data)
    update_fields = prepare_tuple[0]
    query_params = prepare_tuple[1]

    query = f"UPDATE experiences SET {', '.join(update_fields)} WHERE id = %s RETURNING *"
    result = db.execute_one((query, tuple(query_params)))

    if result["result"]:
        return ExperienceInDB(**result["result"][0])
    return None


def delete_applicant_experience(experience_id: uuid.UUID):
    query_tuple = ("DELETE FROM experiences WHERE id = %s", (experience_id,))
    result = db.execute_one(query_tuple)
    if result["affected_rows"]:
        return result["affected_rows"]
    return None


def prepare_fields(id: uuid.UUID, form_data):
    update_fields = []
    query_params = []

    for field, value in form_data.model_dump(exclude_unset=True).items():
        if field == "home_location" and value is not None:
            update_fields.append(f"{field} = point(%s, %s)")
            longitude = value.get("longitude")
            latitude = value.get("latitude")
            query_params.extend([longitude, latitude])
        elif value is not None:
            update_fields.append(f"{field} = %s")
            query_params.append(value)

    query_params.append(id)
    return update_fields, query_params


def insert_applicant_profile(
    account_id: uuid.UUID,
    first_name: str,
    last_name: str,
    education_level_id: int,
    age: int,
    gender: Gender,
    skill_id_list: List[int],
    cv: Union[str, None],
    work_type_id: int,
    seniority_level_id: int,
    position_id: int,
    home_location: Point,
    work_location_max_distance: int,
    contract_type_id: int,
    min_salary: float,
):
    # Common columns and values
    columns = [
        "first_name",
        "last_name",
        "education_level_id",
        "age",
        "gender",
        "skill_id_list",
        "account_id",
        "work_type_id",
        "seniority_level_id",
        "position_id",
        "home_location",
        "work_location_max_distance",
        "contract_type_id",
        "min_salary",
    ]
    values = [
        first_name,
        last_name,
        education_level_id,
        age,
        gender,
        skill_id_list,
        account_id,
        work_type_id,
        seniority_level_id,
        position_id,
        (home_location.get("longitude"), home_location.get("latitude")),
        work_location_max_distance,
        contract_type_id,
        min_salary,
    ]

    if cv:
        columns.append("cv")
        values.append(base64.b64decode(cv))

    query = f"""
        INSERT INTO applicant_profiles ({', '.join(columns)})
        VALUES ({', '.join(['%s'] * len(values))})
        RETURNING *
        """

    result = db.execute_one((query, tuple(values)))
    if result["result"]:
        return ApplicantProfileInDB(**result["result"][0])
    return None


def insert_experiences(experiences: List[CreateExperienceRequest], applicant_account_id: uuid.UUID):
    query = """
        INSERT INTO experiences (company_name, position_id, years, applicant_account_id)
        VALUES (%s, %s, %s, %s)
        """

    query_tuple_list = [
        (
            query,
            (
                experience.company_name,
                experience.position_id,
                experience.years,
                applicant_account_id,
            ),
        )
        for experience in experiences
    ]

    result = db.execute_many(query_tuple_list)
    return result["affected_rows"]
