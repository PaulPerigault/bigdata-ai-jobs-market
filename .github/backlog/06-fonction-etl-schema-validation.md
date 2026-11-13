---
title: "feat(etl): fail fast when the raw CSV does not match the schema"
labels: ["type:fonction", "pkg:etl", "prio:normale", "taille:page"]
milestone: "v0.3.0 Analysis quality"
assignee: PaulPerigault
---

## Context

`spark.read.csv(header=True, schema=RAW_SCHEMA)` silently turns a malformed value into null: a wrong column order or a changed type would flow into the processed tables unnoticed.

## Goal

The ETL stops with a readable message when the header differs from `RAW_SCHEMA` or when more than a stated share of values fail to parse.

## Acceptance criteria

- [ ] A test feeds a CSV with a renamed column and expects a failure naming the column.
- [ ] A test feeds a CSV with unparsable numbers and expects the count of bad values in the message.
- [ ] The counts of the existing cleaning step are unchanged on the sample.

## Package

etl

## Size

page

## Priority

normale

## Milestone

v0.3.0 Analysis quality

## Out of scope

- Rejecting individual rows (they stay counted by `clean`).

## Origin

Rewritten from: a gap found while auditing the cleaning step.

## Definition of done

- [ ] `task verify` is green.
- [ ] Documentation and ADR updated where behaviour or a decision changes.
- [ ] The pull request says `Closes #n` and CI (`ci`) is green.
