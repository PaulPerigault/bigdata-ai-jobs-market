from etl.tables import build_competences, build_metiers, build_offres

CLEANED_ROWS = [
    (
        "J1",
        "AI Engineer",
        "Engineering",
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
        "Engineering",
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
        "J3",
        "Data Scientist",
        "Data",
        "Junior",
        1,
        55000.0,
        50000.0,
        60000.0,
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
    ),
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


def test_build_metiers_is_deterministic_and_deduplicated(spark):
    df_cleaned = spark.createDataFrame(CLEANED_ROWS, COLUMNS)

    metiers_1 = build_metiers(df_cleaned).orderBy("job_title").collect()
    metiers_2 = build_metiers(df_cleaned).orderBy("job_title").collect()

    assert len(metiers_1) == 2  # "AI Engineer" et "Data Scientist" : 2 métiers distincts
    assert [r.metier_id for r in metiers_1] == [r.metier_id for r in metiers_2]
    assert len({r.metier_id for r in metiers_1}) == 2  # pas de collision


def test_build_offres_joins_metier_id(spark):
    df_cleaned = spark.createDataFrame(CLEANED_ROWS, COLUMNS)
    df_metiers = build_metiers(df_cleaned)

    df_offres = build_offres(df_cleaned, df_metiers)

    assert df_offres.count() == 3
    assert df_offres.filter(df_offres.metier_id.isNull()).count() == 0
    assert set(df_offres.columns) == {
        "job_id",
        "metier_id",
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
        "ai_salary_premium_pct",
        "demand_score",
        "posting_year",
        "posting_month",
    }


def test_build_competences_explodes_pipe_separated_skills(spark):
    df_cleaned = spark.createDataFrame(CLEANED_ROWS, COLUMNS)

    df_competences = build_competences(df_cleaned)

    # J1: Python|SQL (2), J2: Python|Cloud (2), J3: SQL (1) => 5 lignes
    assert df_competences.count() == 5
    j1_skills = {
        r.competence for r in df_competences.filter(df_competences.job_id == "J1").collect()
    }
    assert j1_skills == {"Python", "SQL"}


def test_build_competences_deduplicates_repeated_skill_in_same_offer(spark):
    # required_skills liste deux fois "SQL" pour la même offre (trouvé sur
    # le dataset réel, 120 couples job_id/compétence en double sur 9548
    # lignes avant correction) -- explode() sans dropDuplicates()
    # produirait deux lignes identiques (J1, SQL).
    rows = [
        (
            "J1",
            "AI Engineer",
            "Engineering",
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
            "Python|SQL|SQL",
            5.0,
            90,
            2026,
            1,
        )
    ]
    df_cleaned = spark.createDataFrame(rows, COLUMNS)

    df_competences = build_competences(df_cleaned)

    assert df_competences.count() == 2
    skills = {r.competence for r in df_competences.collect()}
    assert skills == {"Python", "SQL"}
