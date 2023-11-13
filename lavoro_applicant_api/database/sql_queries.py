INSERT_APPLICANT_PROFILE_SQL = '''
    INSERT INTO applicant_profiles (
        first_name, last_name, education_level_id, age, gender, skills_id, 
        account_id, cv_url, work_type_id, seniority_level, position_id, 
        home_location, work_location_max_distance, contract_type_id, min_salary
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
'''

INSERT_EXPERIENCE_SQL = '''
    INSERT INTO experiences (company_name, position_id, years, applicant_profile_id)
    VALUES (%s, %s, %s, %s) RETURNING id
'''