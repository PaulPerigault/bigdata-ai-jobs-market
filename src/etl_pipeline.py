"""Pipeline ETL RAW -> processed (offres, metiers, competences).

Lit le CSV RAW depuis HDFS (jamais le disque local, voir CLAUDE.md) à
l'emplacement qui sert aussi de LOCATION à la table Hive externe
projet_ia.ai_jobs_raw. On ne relit pas cette table via `spark.sql`
: Spark, lisant une table Hive TEXTFILE via son propre HiveTableScan,
n'honore pas `skip.header.line.count` (vérifié : la ligne d'en-tête
remonte comme une ligne de données) — `spark.read.csv(header=True)`
gère le header correctement, et reste conforme à HDFS -> Hive/Spark.

Nettoie, construit les 3 tables cibles et les écrit en HDFS
/projet_ia/processed/ avec les tables Hive externes correspondantes.

Usage : docker compose exec jupyter python /home/jovyan/work/etl_pipeline.py
(recette `task etl`).
"""

from etl.cleaning import clean, print_stats
from etl.hive_io import write_processed_table
from etl.schema import RAW_SCHEMA
from etl.spark_session import get_spark
from etl.tables import build_competences, build_metiers, build_offres

PROCESSED_DB = "processed"
PROCESSED_BASE_PATH = "hdfs://namenode:8020/projet_ia/processed"
RAW_CSV_PATH = "hdfs://namenode:8020/projet_ia/raw/ai_jobs_market_2025_2026.csv"


def main() -> None:
    spark = get_spark("etl_pipeline")

    df_raw = spark.read.csv(RAW_CSV_PATH, header=True, schema=RAW_SCHEMA)
    print(f"Lignes lues depuis {RAW_CSV_PATH} : {df_raw.count()}")

    df_cleaned, stats = clean(df_raw)
    print_stats(stats)

    df_metiers = build_metiers(df_cleaned)
    df_offres = build_offres(df_cleaned, df_metiers)
    df_competences = build_competences(df_cleaned)

    print(f"metiers      : {df_metiers.count()} lignes")
    print(f"offres       : {df_offres.count()} lignes")
    print(f"competences  : {df_competences.count()} lignes (job_id x compétence)")

    write_processed_table(
        spark, df_metiers, PROCESSED_DB, "metiers", f"{PROCESSED_BASE_PATH}/metiers"
    )
    write_processed_table(spark, df_offres, PROCESSED_DB, "offres", f"{PROCESSED_BASE_PATH}/offres")
    write_processed_table(
        spark, df_competences, PROCESSED_DB, "competences", f"{PROCESSED_BASE_PATH}/competences"
    )

    print("OK : tables processed.offres / processed.metiers / processed.competences écrites.")


if __name__ == "__main__":
    main()
