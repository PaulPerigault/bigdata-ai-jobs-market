from etl.cleaning import clean
from etl.tables import build_competences, build_metiers, build_offres

RAW_ROWS = [
    (
        "J1",
        "AI Engineer",
        "Eng",
        "Senior",
        7,
        150000.0,
        120000.0,
        180000.0,
        "Paris",
        "France",
        "Remote",
        "Startup",
        "Tech",
        "Python|SQL",
        5.0,
        90,
        2026,
        1,
    ),
    (
        "J2",
        "AI Engineer",
        "Eng",
        "Mid",
        3,
        90000.0,
        80000.0,
        100000.0,
        "Lyon",
        "France",
        "Hybrid",
        "Enterprise",
        "Finance",
        "Python|Cloud",
        2.0,
        60,
        2026,
        2,
    ),
    (
        "J2",
        "AI Engineer",
        "Eng",
        "Mid",
        3,
        90000.0,
        80000.0,
        100000.0,
        "Lyon",
        "France",
        "Hybrid",
        "Enterprise",
        "Finance",
        "Python|Cloud",
        2.0,
        60,
        2026,
        2,
    ),  # doublon
    (
        "J3",
        "Data Scientist",
        "Data",
        "Junior",
        1,
        -5.0,
        0.0,
        0.0,
        "Berlin",
        "Germany",
        "On-site",
        "SME",
        "Health",
        "SQL",
        1.0,
        40,
        2025,
        11,
    ),  # salaire invalide
]
COLUMNS = [
    "job_id",
    "job_title",
    "job_category",
    "experience_level",
    "years_of_experience",
    "annual_salary_usd",
    "salary_min_usd",
    "salary_max_usd",
    "city",
    "country",
    "remote_work",
    "company_size",
    "industry",
    "required_skills",
    "ai_salary_premium_pct",
    "demand_score",
    "posting_year",
    "posting_month",
]


def test_row_counts_are_consistent_across_the_pipeline(spark):
    df_raw = spark.createDataFrame(RAW_ROWS, COLUMNS)

    df_cleaned, stats = clean(df_raw)
    n_cleaned = df_cleaned.count()

    assert stats["total_rows_before"] == 4
    assert n_cleaned == 2  # doublon + salaire<=0 retirés

    df_offres = build_offres(df_cleaned, build_metiers(df_cleaned))
    assert df_offres.count() == n_cleaned  # 1 ligne offre par ligne cleaned, jamais plus

    df_competences = build_competences(df_cleaned)
    assert df_competences.count() >= n_cleaned  # >= 1 compétence par offre

    df_metiers = build_metiers(df_cleaned)
    assert df_metiers.count() <= n_cleaned  # référentiel dédupliqué par job_title
