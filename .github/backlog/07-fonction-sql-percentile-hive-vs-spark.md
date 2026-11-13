---
title: "test(sql): record the Hive versus Spark SQL results of the median"
labels: ["type:fonction", "pkg:sql", "prio:normale", "taille:page"]
milestone: "v0.3.0 Analysis quality"
assignee: PaulPerigault
---

## Context

The median salary from `PERCENTILE_APPROX` is 179421 on Hive and 180000 on Spark SQL for the same table (project notes). The difference is documented in prose only.

## Goal

The difference is reproduced by a test or a notebook cell on the synthetic sample, with the explanation attached.

## Acceptance criteria

- [ ] A test or cell computes the median with both engines on the sample and asserts the documented relation (equal for `AVG` and `COUNT`, tolerance stated for the percentile).
- [ ] Chapter 8 of the report points to it.
- [ ] It runs under `task test` without Hive, or is marked as needing the stack.

## Package

sql

## Size

page

## Priority

normale

## Milestone

v0.3.0 Analysis quality

## Out of scope

- Choosing which engine is right.

## Origin

Rewritten from: the nuance noted in the project notes.

## Definition of done

- [ ] `task verify` is green.
- [ ] Documentation and ADR updated where behaviour or a decision changes.
- [ ] The pull request says `Closes #n` and CI (`ci`) is green.
