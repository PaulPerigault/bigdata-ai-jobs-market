---
title: "ci(report): build the report in CI with the pinned image"
labels: ["type:fonction", "pkg:report", "prio:basse", "taille:page"]
milestone: "v0.3.0 Analysis quality"
assignee: PaulPerigault
---

## Context

`task report` builds the French report with XeLaTeX in a container pinned by digest. It has not been run since the rebuild, and nothing checks that it still compiles after a change.

## Goal

A CI job compiles the report and fails on a LaTeX error; the PDF is kept as a short-lived artifact.

## Acceptance criteria

- [ ] `task report` produces `report/main.pdf` locally (page count noted in the pull request).
- [ ] The CI job uses the same pinned image and uploads the PDF with a retention of seven days.
- [ ] The `ci` aggregate lists the job.

## Package

report

## Size

page

## Priority

basse

## Milestone

v0.3.0 Analysis quality

## Out of scope

- Translating the report to English.
- Publishing the PDF.

## Origin

Rewritten from: the report build of the original project.

## Definition of done

- [ ] `task verify` is green.
- [ ] Documentation and ADR updated where behaviour or a decision changes.
- [ ] The pull request says `Closes #n` and CI (`ci`) is green.
