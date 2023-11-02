CREATE EXTENSION "uuid-ossp";

CREATE TYPE gender AS ENUM ('male', 'female', 'other');

CREATE TABLE IF NOT EXISTS applicant_profiles (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    education_level_id uuid REFERENCES education_catalog(id) ON DELETE RESTRICT,
    age SMALLINT CHECK (age > 0),
    gender gender,
    skills_id uuid REFERENCES skills_catalog(id) ON DELETE RESTRICT,
    account_id uuid REFERENCES accounts(id) ON DELETE CASCADE,
    cv_url VARCHAR(255),
    work_type_id uuid REFERENCES work_type_catalog(id) ON DELETE RESTRICT,
    seniority_level SMALLINT,
    position_id uuid REFERENCES position_catalog(id) ON DELETE RESTRICT,
    home_location POINT,
    work_location_max_distance INT,
    contract_type_id uuid REFERENCES contract_type_catalog(id) ON DELETE RESTRICT,
    min_salary REAL
);

CREATE TABLE IF NOT EXISTS experiences (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    company_name VARCHAR(64) NOT NULL,
    position_id uuid NOT NULL REFERENCES position_catalog(id) ON DELETE RESTRICT,
    years SMALLINT,
    applicant_profile_id uuid NOT NULL REFERENCES applicant_profiles(id) ON DELETE CASCADE
);
