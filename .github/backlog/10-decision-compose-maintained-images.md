---
title: "decision(compose): move to maintained Hadoop, Hive and Spark images?"
labels: ["type:decision", "pkg:compose", "prio:normale", "taille:cahier"]
milestone: "v0.4.0 Modern stack"
assignee: PaulPerigault
---

## Context

The stack runs Hadoop 2.7.4 and Hive 2.3.2 images that are unmaintained, amd64 only (emulated on Apple Silicon) and vulnerable (SECURITY.md). Spark 3.5.0 pairs with Java 17; Spark 4 changes the supported Java and Python versions.

## Goal

A decision, written as an ADR, on the target set (Hadoop 3, Hive 4, Spark 4 or a lighter alternative) with the cost of migrating the SQL, the tests and the notebook.

## Acceptance criteria

- [ ] Candidate image sets are listed with their maintenance status and architectures, checked on the registries on the day.
- [ ] One candidate is proven on the demo, or the ADR says why none is.
- [ ] The ADR gives the risk and the way back, and splits the migration into issues of at most one session.

## Package

compose

## Size

cahier

## Priority

normale

## Milestone

v0.4.0 Modern stack

## Out of scope

- Doing the migration in this issue.

## Origin

Rewritten from: the known weaknesses recorded in ADR 0004.

## Definition of done

- [ ] `task verify` is green.
- [ ] Documentation and ADR updated where behaviour or a decision changes.
- [ ] The pull request says `Closes #n` and CI (`ci`) is green.
