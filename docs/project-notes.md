# Project notes: technical decisions of the original project

Condensed from the working notes of the original coursework (September 2026), kept because the code,
the notebook and the report refer to them. They describe what was observed on the original machines;
anything not re-run since is marked in the README "Limits".

## Scope

Course deliverable: HDFS ingestion, Hive tables (RAW and processed), Spark cleaning, a three-table model, Hive SQL
and Spark SQL queries, at least six visualizations in a Jupyter notebook, and a written report. Jupyter/PySpark
replaced the Zeppelin suggested by the assignment, as agreed with the course supervisor. HDFS and Hive stay in the chain:
the notebook reads HDFS and Hive, never the local CSV.

## Pipeline (RAW to processed)

- `src/etl/schema.py` holds the RAW schema, `cleaning.py` the cleaning with before/after counts, `tables.py` the
  three tables, `hive_io.py` writes Parquet to HDFS and derives the `CREATE EXTERNAL TABLE` from the Spark schema.
- `metier_id` is `sha2(job_title, 256)` truncated to 16 characters: stable between runs, unlike
  `monotonically_increasing_id()`.
- `etl_pipeline.py` reads the CSV straight from HDFS with `spark.read.csv(header=True, schema=...)`. Reading the
  Hive TEXTFILE table through `spark.sql` does not honour `skip.header.line.count` (the header came back as a data
  row: 1501 rows instead of 1500). The Hive RAW table stays the entry point of the Hive SQL queries.
- Reference figures on the real dataset: 1500 raw rows, 0 duplicate `job_id`, 0 salary at or below 0, 25 distinct
  job titles, 1500 offers, 9428 distinct (offer, skill) pairs.

## Bugs found and fixed during the project

- `spark-submit`, not `python`, runs the ETL in the Jupyter container: `docker compose exec` does not inherit the
  `PYTHONPATH` that the image sets only for the Jupyter server process (`No module named 'pyspark'`).
- `processed.competences` had 9548 rows for 9428 distinct pairs: `required_skills` sometimes lists a skill twice
  (`Python|SQL|SQL`), and `explode(split(...))` kept both. Fixed with `dropDuplicates(["job_id", "competence"])`
  and a dedicated test; the top-skills dashboard had shown inflated counts (SQL 452 instead of 422).
- Ties in "top skills" need a secondary sort (`ORDER BY nb_offres DESC, competence ASC`), otherwise the fifth rank
  was not reproducible between runs.
- `PERCENTILE_APPROX` does not return the same value on Hive and on Spark SQL for the same table (median salary
  179421 on Hive, 180000 on Spark SQL). The two engines agree on `AVG` and `COUNT`, not on approximate percentiles.

## Stack choices

- Hadoop 2.7.4 images (`bde2020`), because the Hive 2.3.2 image is built for that version. Web ports are 50070 and
  50075 (not the Hadoop 3 ports). The images exist for amd64 only: on Apple Silicon they run emulated, and
  `JAVA_TOOL_OPTIONS=-Xint` avoids multi-minute JIT stalls under emulation.
- The metastore database is the official `postgres:13.18`, which starts empty: `scripts/hive-metastore-entrypoint.sh`
  runs `schematool -initSchema` and then the metastore. It must stay a single token in `command:` because the image
  entrypoint runs `exec $@` unquoted.
- `jupyter/pyspark-notebook:spark-3.5.0` for Spark and the notebook. Tests use `pyspark==3.5.0`, which needs Java 11
  or 17 and, on Windows, CPython 3.11 (see ADR 0003).
- The report is built with XeLaTeX in a pinned `texlive` container; the fonts are versioned (Apache and OFL
  licences) so that the build does not depend on system fonts.
