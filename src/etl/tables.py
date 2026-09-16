from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def build_metiers(df_cleaned: DataFrame) -> DataFrame:
    """Référentiel des métiers distincts.

    metier_id est un hash déterministe (sha2(job_title, 256) tronqué à 16
    caractères hex) et non monotonically_increasing_id() : ce dernier
    n'est stable ni entre exécutions ni entre partitions (CLAUDE.md).
    """
    return (
        df_cleaned.select("job_title", "job_category")
        .distinct()
        .withColumn("metier_id", F.substring(F.sha2(F.col("job_title"), 256), 1, 16))
    )


def build_offres(df_cleaned: DataFrame, df_metiers: DataFrame) -> DataFrame:
    return df_cleaned.join(
        df_metiers.select("job_title", "metier_id"), on="job_title", how="left"
    ).select(
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
    )


def build_competences(df_cleaned: DataFrame) -> DataFrame:
    return df_cleaned.select(
        F.col("job_id"),
        F.explode(F.split(F.col("required_skills"), "\\|")).alias("competence"),
    )
