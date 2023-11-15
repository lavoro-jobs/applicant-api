import uuid
from typing import List

from lavoro_applicant_api.database import db
from lavoro_library.models import CreateExperienceRequest, Gender, Point


def get_applicant_profile(account_id: uuid.UUID):
    query_tuple = ("SELECT * FROM applicant_profiles WHERE account_id = %s", (account_id,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return result["result"][0]
    else:
        return None


def insert_applicant_profile(
    account_id: uuid.UUID,
    first_name: str,
    last_name: str,
    education_level_id: int,
    age: int,
    gender: Gender,
    skills_id: List[int],
    cv_url: str,
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
            first_name, last_name, education_level_id, age, gender, skills_id, account_id,
            work_type_id, seniority_level, position_id, home_location, work_location_max_distance,
            contract_type_id, min_salary)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
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
            skills_id,
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
        return result["result"][0]["id"]
    return None


def insert_experiences(experiences: List[CreateExperienceRequest], applicant_profile_id: uuid.UUID):
    query = """
        INSERT INTO experiences (company_name, position_id, years, applicant_profile_id)
        VALUES (%s, %s, %s, %s)
        """

    query_tuple_list = [
        (query, (experience.company_name, experience.position_id, experience.years, applicant_profile_id))
        for experience in experiences
    ]

    result = db.execute_many(query_tuple_list)
    return result["affected_rows"]
