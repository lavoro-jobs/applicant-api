CREATE EXTENSION "uuid-ossp";

CREATE TYPE gender AS ENUM ('male', 'female', 'other');

CREATE TABLE IF NOT EXISTS applicant_profiles (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    education_level_id uuid,
    age SMALLINT CHECK (age > 0),
    gender gender,
    skills_id uuid,
    account_id uuid NOT NULL,
    cv_url VARCHAR(255),
    work_type_id uuid,
    seniority_level SMALLINT,
    position_id uuid,
    home_location POINT,
    work_location_max_distance INT,
    contract_type_id uuid,
    min_salary REAL
);

CREATE TABLE IF NOT EXISTS experiences (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    company_name VARCHAR(64) NOT NULL,
    position_id uuid NOT NULL,
    years SMALLINT,
    applicant_profile_id uuid NOT NULL REFERENCES applicant_profiles(id) ON DELETE CASCADE
);
