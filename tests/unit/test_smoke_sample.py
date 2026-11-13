"""Smoke test: the whole RAW -> processed chain on the synthetic sample, without HDFS or Hive."""

import csv

import gen_sample

from etl.cleaning import clean
from etl.schema import RAW_SCHEMA
from etl.tables import build_competences, build_metiers, build_offres


def expected_skill_pairs() -> int:
    """Distinct (job_id, skill) pairs, counted in plain Python from the CSV."""
    with gen_sample.OUT.open(newline="", encoding="utf-8") as f:
        return sum(len(set(r["required_skills"].split("|"))) for r in csv.DictReader(f))


def test_pipeline_on_the_sample(spark):
    raw = spark.read.csv(str(gen_sample.OUT), header=True, schema=RAW_SCHEMA)
    assert raw.count() == gen_sample.ROWS  # the header is not read as a data row

    cleaned, stats = clean(raw)
    assert stats["duplicates_removed"] == 0
    assert stats["rows_removed_non_positive"] == 0

    metiers = build_metiers(cleaned)
    offres = build_offres(cleaned, metiers)
    competences = build_competences(cleaned)

    assert metiers.count() == len(gen_sample.TITLES)
    assert offres.count() == gen_sample.ROWS
    assert offres.filter("metier_id IS NULL").count() == 0  # every offer joins a job title
    assert competences.count() == expected_skill_pairs()
