"""The synthetic sample: reproducible, and shaped like the real dataset. No Spark needed."""

import csv
from pathlib import Path

import gen_sample

from etl.schema import RAW_SCHEMA

SAMPLE = Path(gen_sample.OUT)


def read_rows() -> list[dict[str, str]]:
    with SAMPLE.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_committed_sample_equals_the_generator_output():
    assert SAMPLE.read_bytes().decode("utf-8") == gen_sample.render()


def test_sample_header_is_the_raw_schema():
    with SAMPLE.open(newline="", encoding="utf-8") as f:
        header = next(csv.reader(f))
    assert header == [field.name for field in RAW_SCHEMA.fields]


def test_sample_has_unique_ids_and_valid_salaries():
    rows = read_rows()
    assert len(rows) == gen_sample.ROWS
    assert len({r["job_id"] for r in rows}) == gen_sample.ROWS
    assert all(float(r["annual_salary_usd"]) > 0 for r in rows)


def test_sample_repeats_one_skill_in_one_offer():
    skills = read_rows()[gen_sample.DUPLICATE_SKILLS_ROW]["required_skills"].split("|")
    assert len(skills) != len(set(skills))
