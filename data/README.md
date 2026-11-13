# Data

## The real dataset (not in this repository)

| | |
| --- | --- |
| Name | AI Jobs Market 2025-2026 \| Salaries |
| Source | Kaggle, <https://www.kaggle.com/datasets/alitaqishah/ai-jobs-market-2025-2026-salaries> (free account needed) |
| File | `ai_jobs_market_2025_2026.csv`, 1500 rows, 25 columns, 383 900 bytes |
| SHA-256 | `6ae7bc7bf724250cd8c977f86b620128318070a23cb0b17340e58d2321f7864e` |
| Licence | **not verified**: the public page, read on 2026-11-13, does not state it |
| Personal data | none: job titles, categories, cities and countries, salary ranges, skills; no names or contact details |
| Provenance | the file used by the original coursework; whether the values are real or synthetic is not stated by the source |

Because the licence is not verified, the file is **not redistributed here** ([ADR 0002](../docs/adr/0002-synthetic-sample-instead-of-the-dataset.md)).
To work with it: download it, put it at `data/raw/ai_jobs_market_2025_2026.csv` (ignored by Git), then run

```
task data:raw:check
task ingest
```

`task data:raw:check` compares the SHA-256, the size and the line count with the values above, so a different or
truncated file is refused before it reaches HDFS.

## The synthetic sample (in this repository)

`data/sample/ai_jobs_sample.csv`: 60 invented rows with the same 25 columns, produced by `data/gen_sample.py` with a fixed seed.
Job titles start with `Sample` and ids with `SAMPLE`. One row lists a skill twice on purpose (the bug that the
`dropDuplicates` of `build_competences` fixes). No value comes from the real dataset.

```
task data:gen      regenerate it
task data:check    fail if the committed file differs from the generator
```

It drives the smoke test (`tests/unit/test_smoke_sample.py`) and `task demo`. Its figures say nothing about the job market.
