from etl.cleaning import clean

RAW_ROWS = [
    ("J1", "AI Engineer", "Senior", 150000.0, "USA", "Python|SQL"),
    ("J1", "AI Engineer", "Senior", 150000.0, "USA", "Python|SQL"),  # doublon job_id
    ("J2", "Data Scientist", "Mid", -10.0, "France", "Python"),  # salaire invalide
    ("J3", None, "Junior", 60000.0, "UK", None),  # job_title/required_skills NULL
]
COLUMNS = [
    "job_id",
    "job_title",
    "experience_level",
    "annual_salary_usd",
    "country",
    "required_skills",
]


def test_clean_removes_duplicates_and_invalid_salaries(spark):
    df_raw = spark.createDataFrame(RAW_ROWS, COLUMNS)

    df_cleaned, stats = clean(df_raw)

    assert stats["total_rows_before"] == 4
    assert stats["duplicate_job_ids_before"] == 1
    assert stats["total_rows_after_dedup"] == 3
    assert stats["duplicates_removed"] == 1
    assert stats["rows_removed_salary_leq_0"] == 1
    assert stats["total_rows_after"] == 2

    remaining_ids = {row.job_id for row in df_cleaned.select("job_id").collect()}
    assert remaining_ids == {"J1", "J3"}


def test_clean_fills_missing_job_title_and_skills(spark):
    df_raw = spark.createDataFrame(RAW_ROWS, COLUMNS)

    df_cleaned, _ = clean(df_raw)

    j3 = df_cleaned.filter(df_cleaned.job_id == "J3").collect()[0]
    assert j3.job_title == "Unknown"
    assert j3.required_skills == "Unknown"
