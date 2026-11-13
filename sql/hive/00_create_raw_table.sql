-- Table externe Hive sur la zone RAW HDFS. Aucun champ ne contient de
-- virgule/quote (vérifié sur le CSV réel : 24 virgules sur chaque ligne),
-- un SerDe délimité simple suffit, pas besoin d'OpenCSVSerde.
CREATE DATABASE IF NOT EXISTS projet_ia;

CREATE EXTERNAL TABLE IF NOT EXISTS projet_ia.ai_jobs_raw (
    job_id STRING,
    job_title STRING,
    job_category STRING,
    experience_level STRING,
    years_of_experience INT,
    education_required STRING,
    annual_salary_usd DOUBLE,
    salary_min_usd DOUBLE,
    salary_max_usd DOUBLE,
    city STRING,
    country STRING,
    remote_work STRING,
    company_size STRING,
    industry STRING,
    required_skills STRING,
    ai_salary_premium_pct DOUBLE,
    demand_score INT,
    demand_growth_yoy_pct DOUBLE,
    benefits_score_10 DOUBLE,
    posting_year INT,
    posting_month INT,
    is_senior INT,
    is_remote_friendly INT,
    is_llm_role INT,
    salary_tier STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/projet_ia/raw'
TBLPROPERTIES ('skip.header.line.count' = '1');
