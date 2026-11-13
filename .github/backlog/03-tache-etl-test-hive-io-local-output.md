---
title: "test(etl): cover the Hive and HDFS output with a local file system"
labels: ["type:tache", "pkg:etl", "prio:normale", "taille:page"]
milestone: "v0.2.0 Reproducible local run"
assignee: PaulPerigault
---

## Context

`write_processed_table` (Parquet on HDFS, then `CREATE EXTERNAL TABLE`) is the only part of the pipeline without a test: the unit tests run Spark `local[2]` without Hive.

## Goal

`hive_io` has a test that writes to a temporary local path and checks the generated DDL, without HDFS or a metastore.

## Acceptance criteria

- [ ] A test asserts the DDL generated for the three processed tables (column names, Hive types, `STORED AS PARQUET`).
- [ ] The test does not need the stack and closes everything it opens (it passes on Windows).
- [ ] `task test` stays under two minutes.

## Package

etl

## Size

page

## Priority

normale

## Milestone

v0.2.0 Reproducible local run

## Out of scope

- Testing against a real metastore.
- Changing the generated DDL.

## Origin

Rewritten from: a gap found while auditing the tests of the original project.

## Definition of done

- [ ] `task verify` is green.
- [ ] Documentation and ADR updated where behaviour or a decision changes.
- [ ] The pull request says `Closes #n` and CI (`ci`) is green.
