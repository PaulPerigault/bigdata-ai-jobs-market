---
title: "ci: first green run of every job on GitHub runners"
labels: ["type:tache", "pkg:ci", "prio:haute", "taille:page"]
milestone: "v0.2.0 Reproducible local run"
assignee: PaulPerigault
---

## Context

The CI was written and every check was run locally through `task`, but no workflow has run on a GitHub runner yet. The Spark job (Java 17, `REQUIRE_SPARK=1`), `zizmor`, `codeql`, `compose:check` and the Trivy scan are the most likely to show something the author's machine did not.

## Goal

`ci` is green on `main` and on a pull request, and what the runners revealed is written down.

## Acceptance criteria

- [ ] `gh run list --workflow ci.yml --branch main --limit 1 --json conclusion` reports `success`.
- [ ] The `test` job runs 12 tests and skips none (no `SKIPPED` line in its log).
- [ ] `zizmor` reports no finding, or each finding is fixed in the workflow.
- [ ] `docs/journal/` has a dated note listing every fix the first runs needed.

## Package

ci

## Size

page

## Priority

haute

## Milestone

v0.2.0 Reproducible local run

## Out of scope

- Adding jobs that do not exist yet.
- Removing a check to get a green run.

## Origin

Rewritten from: the CI of the original coursework repository.

## Definition of done

- [ ] `task verify` is green.
- [ ] Documentation and ADR updated where behaviour or a decision changes.
- [ ] The pull request says `Closes #n` and CI (`ci`) is green.
