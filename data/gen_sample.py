"""Deterministic synthetic sample with the schema of the AI job-market dataset.

The real dataset is not redistributed (its licence is not stated on its public page, see
data/README.md). This sample has the same 25 columns, 60 invented rows and a fixed seed, so the
smoke test and `task demo` run offline. Every value is invented: none comes from the real data.

    python data/gen_sample.py            write data/sample/ai_jobs_sample.csv
    python data/gen_sample.py --check    fail if the committed file differs from the generator
"""

import argparse
import random
import sys
from pathlib import Path

SEED = 2026
ROWS = 60
OUT = Path(__file__).parent / "sample" / "ai_jobs_sample.csv"

HEADER = [
    "job_id", "job_title", "job_category", "experience_level", "years_of_experience",
    "education_required", "annual_salary_usd", "salary_min_usd", "salary_max_usd", "city",
    "country", "remote_work", "company_size", "industry", "required_skills",
    "ai_salary_premium_pct", "demand_score", "demand_growth_yoy_pct", "benefits_score_10",
    "posting_year", "posting_month", "is_senior", "is_remote_friendly", "is_llm_role",
    "salary_tier",
]  # fmt: skip

TITLES = [
    ("Sample ML Engineer", "AI Engineering"),
    ("Sample Data Scientist", "Data Science"),
    ("Sample Prompt Designer", "AI Engineering"),
    ("Sample MLOps Engineer", "Infrastructure"),
    ("Sample AI Researcher", "Research"),
    ("Sample Data Analyst", "Analytics"),
]
LEVELS = [("Entry (0-2 yrs)", 1, 2), ("Mid (3-5 yrs)", 3, 5), ("Senior (6-9 yrs)", 6, 9)]
PLACES = [("Paris", "France"), ("Berlin", "Germany"), ("Austin", "USA"), ("Toronto", "Canada")]
REMOTE = ["On-site", "Hybrid", "Fully Remote"]
SIZES = ["Startup (1-50)", "SME (51-500)", "Enterprise (5000+)"]
INDUSTRIES = ["Finance", "Health", "Retail", "Energy"]
SKILLS = ["Python", "SQL", "Cloud", "Spark", "NLP", "Testing", "APIs", "Leadership"]
DUPLICATE_SKILLS_ROW = 6  # "Python|SQL|SQL": the same skill listed twice in one offer


def tier(salary: int) -> str:
    bounds = [
        (100_000, "Entry (<$100k)"),
        (150_000, "Mid ($100-150k)"),
        (200_000, "Upper-Mid ($150-200k)"),
    ]
    return next((label for limit, label in bounds if salary < limit), "Senior ($200-300k)")


def build_rows() -> list[list[str]]:
    rng = random.Random(SEED)
    rows = []
    for i in range(ROWS):
        title, category = TITLES[i % len(TITLES)]
        level, lo, hi = LEVELS[rng.randrange(len(LEVELS))]
        city, country = PLACES[rng.randrange(len(PLACES))]
        salary = rng.randrange(90, 260) * 1000
        skills = "|".join(rng.sample(SKILLS, rng.randrange(3, 6)))
        if i == DUPLICATE_SKILLS_ROW:
            skills = "Python|SQL|SQL"
        rows.append([
            f"SAMPLE{i + 1:04d}", title, category, level, str(rng.randrange(lo, hi + 1)),
            "Master's", f"{salary}.0", str(salary - 20_000), str(salary + 30_000), city, country,
            REMOTE[rng.randrange(3)], SIZES[rng.randrange(3)], INDUSTRIES[rng.randrange(4)],
            skills, f"{rng.randrange(30, 180) / 10:.1f}", str(rng.randrange(68, 99)),
            f"{rng.randrange(50, 880) / 10:.1f}", f"{rng.randrange(60, 98) / 10:.1f}",
            str(2025 + i % 2), str(1 + i % 12), str(int(level.startswith("Senior"))), "1", "0",
            tier(salary),
        ])  # fmt: skip
    return rows


def render() -> str:
    lines = [",".join(HEADER)] + [",".join(row) for row in build_rows()]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        current = OUT.read_bytes().decode("utf-8") if OUT.exists() else ""
        if current != expected:
            print(f"{OUT} differs from the generator: run `task data:gen`", file=sys.stderr)
            return 1
        print(f"{OUT}: matches the generator ({ROWS} rows, seed {SEED})")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(expected.encode("utf-8"))
    print(f"wrote {OUT} ({ROWS} rows, seed {SEED})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
