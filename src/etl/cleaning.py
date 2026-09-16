from pyspark.sql import DataFrame
from pyspark.sql import functions as F

IMPORTANT_COLUMNS = [
    "job_id",
    "job_title",
    "annual_salary_usd",
    "experience_level",
    "country",
    "required_skills",
]


def null_counts(df: DataFrame, columns: list[str]) -> dict[str, int]:
    agg = df.select([F.sum(F.col(c).isNull().cast("int")).alias(c) for c in columns])
    row = agg.collect()[0]
    return {c: row[c] for c in columns}


def clean(df_raw: DataFrame) -> tuple[DataFrame, dict]:
    """Nettoie le DataFrame RAW et retourne (df_cleaned, stats).

    stats contient les comptages avant/après demandés par CLAUDE.md :
    NULLs par colonne importante, doublons sur job_id, lignes filtrées
    sur salaire <= 0.
    """
    stats: dict = {}

    stats["total_rows_before"] = df_raw.count()
    stats["nulls_before"] = null_counts(df_raw, IMPORTANT_COLUMNS)

    stats["duplicate_job_ids_before"] = (
        df_raw.groupBy("job_id").count().filter(F.col("count") > 1).count()
    )
    df_dedup = df_raw.dropDuplicates(["job_id"])
    stats["total_rows_after_dedup"] = df_dedup.count()
    stats["duplicates_removed"] = stats["total_rows_before"] - stats["total_rows_after_dedup"]

    rows_before_salary_filter = df_dedup.count()
    df_filtered = df_dedup.filter(F.col("annual_salary_usd") > 0)
    stats["rows_removed_salary_leq_0"] = rows_before_salary_filter - df_filtered.count()

    df_cleaned = df_filtered.na.fill({"required_skills": "Unknown", "job_title": "Unknown"})

    stats["total_rows_after"] = df_cleaned.count()
    stats["nulls_after"] = null_counts(df_cleaned, IMPORTANT_COLUMNS)

    return df_cleaned, stats


def print_stats(stats: dict) -> None:
    print("=== Nettoyage : comptages avant/après ===")
    print(f"Lignes RAW               : {stats['total_rows_before']}")
    print(f"Doublons job_id détectés : {stats['duplicate_job_ids_before']}")
    print(
        f"Lignes après dropDuplicates(job_id) : {stats['total_rows_after_dedup']} "
        f"({stats['duplicates_removed']} lignes supprimées)"
    )
    print(f"Lignes filtrées (annual_salary_usd <= 0) : {stats['rows_removed_salary_leq_0']}")
    print(f"Lignes finales après nettoyage : {stats['total_rows_after']}")
    print("NULLs par colonne (avant -> après) :")
    for col in IMPORTANT_COLUMNS:
        print(f"  {col:25s} {stats['nulls_before'][col]:5d} -> {stats['nulls_after'][col]:5d}")
