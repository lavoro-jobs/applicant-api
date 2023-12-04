import uuid
from typing import List, Union

from lavoro_applicant_api.database import db
from lavoro_library.models import ApplicantProfileInDB, CreateExperienceRequest, Gender, Experience, \
    Point, UpdateApplicantProfileRequest, UpdateApplicantExperienceRequest, ExperienceInDB


def get_applicant_profile(account_id: uuid.UUID):
    query_tuple = ("SELECT * FROM applicant_profiles WHERE account_id = %s", (account_id,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return ApplicantProfileInDB(**result["result"][0])
    else:
        return None


def get_applicant_experiences(account_id: uuid.UUID):
    query_tuple = ("SELECT * FROM experiences WHERE applicant_account_id = %s", (account_id,))
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
    result = update_model("experiences", account_id, form_data)

    if result["result"]:
        return ExperienceInDB(**result["result"][0])
    return None


def update_applicant_experience(experience_id: uuid.UUID, form_data: UpdateApplicantExperienceRequest):
    result = update_model("experiences", experience_id, form_data)

    if result["result"]:
        return ExperienceInDB(**result["result"][0])
    return None


def update_model(table_name: str, id: uuid.UUID, form_data):
    update_fields = []
    query_params = []

    for field, value in form_data.model_dump(exclude_unset=True).items():
        if value is not None:
            update_fields.append(f"{field} = %s")
            query_params.append(value)

    query_params.append(id)
    query = f"UPDATE {table_name} SET {', '.join(update_fields)} WHERE id = %s RETURNING *"
    result = db.execute_one((query, tuple(query_params)))

    return result


def insert_applicant_profile(
    account_id: uuid.UUID,
    first_name: str,
    last_name: str,
    education_level_id: int,
    age: int,
    gender: Gender,
    skill_id_list: List[int],
    cv: Union[bytes, None],
    work_type_id: int,
    seniority_level_id: int,
    position_id: int,
    home_location: Point,
    work_location_max_distance: int,
    contract_type_id: int,
    min_salary: float,
):
    query = """
        INSERT INTO applicant_profiles (
            first_name, last_name, education_level_id, age, gender, skill_id_list, account_id,
            work_type_id, seniority_level_id, position_id, home_location, work_location_max_distance,
            contract_type_id, min_salary)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """

    point = (home_location.get("longitude"), home_location.get("latitude"))

    query_tuple = (
        query,
        (
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
            point,
            work_location_max_distance,
            contract_type_id,
            min_salary,
        ),
    )

    result = db.execute_one(query_tuple)
    if result["result"]:
        return ApplicantProfileInDB(**result["result"][0])
    return None


def insert_experiences(experiences: List[CreateExperienceRequest], applicant_account_id: uuid.UUID):
    query = """
        INSERT INTO experiences (company_name, position_id, years, applicant_account_id)
        VALUES (%s, %s, %s, %s)
        """

    query_tuple_list = [
        (query, (experience.company_name, experience.position_id, experience.years, applicant_account_id))
        for experience in experiences
    ]

    result = db.execute_many(query_tuple_list)
    return result["affected_rows"]
