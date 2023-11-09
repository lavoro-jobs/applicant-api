from collections import defaultdict
from typing import List

from lavoro_applicant_api.database import db
from lavoro_library.models import ApplicantProfileDto, ApplicantProfile, Experience, Point


def get_applicant_profiles() -> List[ApplicantProfileDto]:
    query_tuple = ("""
        SELECT 
            ap.id AS id,
            ap.first_name AS first_name,
            ap.last_name AS last_name,
            ap.education_level_id AS education_level_id,
            ap.age AS age,
            ap.gender AS gender,
            ap.skills_id AS skills_id,
            ap.account_id AS account_id,
            ap.cv_url AS cv_url,
            ap.work_type_id AS work_type_id,
            ap.seniority_level AS seniority_level,
            ap.position_id AS position_id,
            ap.home_location AS home_location,
            ap.work_location_max_distance AS work_location_max_distance,
            ap.contract_type_id AS contract_type_id,
            ap.min_salary AS min_salary,
            exp.id AS experience_id,
            exp.company_name AS experience_company_name,
            exp.position_id AS experience_position_id,
            exp.years AS experience_years,
            exp.applicant_profile_id AS experience_applicant_profile_id
        FROM 
            applicant_profiles ap
        LEFT JOIN experiences exp
            ON ap.id = exp.applicant_profile_id;
                   """, None)

    result = db.execute_one(query_tuple)

    applicants = {}

    for row in result['result']:
        applicant_id = row['id']

        # Initialize the applicant profile if it's not already in the dictionary
        if applicant_id not in applicants:
            applicant_data = {
                'id': row['id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'education_level_id': row['education_level_id'],
                'age': row['age'],
                'gender': row['gender'],
                'skills_id': row['skills_id'],
                'account_id': row['account_id'],
                'cv_url': row['cv_url'],
                'home_location': row['home_location'],
                'work_type_id': row['work_type_id'],
                'seniority_level': row['seniority_level'],
                'position_id': row['position_id'],
                'work_location_max_distance': row['work_location_max_distance'],
                'contract_type_id': row['contract_type_id'],
                'min_salary': row['min_salary'],
                'experiences': []
            }
            applicants[applicant_id] = ApplicantProfileDto(**applicant_data)

        # Add experience to the applicant profile if it exists
        if row['experience_id']:
            experience_data = {
                'id': row['experience_id'],
                'company_name': row['experience_company_name'],
                'position_id': row['experience_position_id'],
                'years': row['experience_years'],
                'applicant_profile_id': row['experience_applicant_profile_id']
            }
            applicants[applicant_id].experiences.append(Experience(**experience_data))

    # Convert dictionary to list and return it
    return list(applicants.values())
