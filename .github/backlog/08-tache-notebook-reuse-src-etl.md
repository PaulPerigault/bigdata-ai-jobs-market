---
title: "refactor(notebook): call src/etl instead of repeating its logic"
labels: ["type:tache", "pkg:notebook", "prio:basse", "taille:page"]
milestone: "v0.3.0 Analysis quality"
assignee: PaulPerigault
---

## Context

The notebook rebuilds a schema and some transformations in its own cells; the rule of the project is that logic lives in `src/etl/` and the notebook calls it.

## Goal

The notebook imports `etl.schema` and the table builders where it currently duplicates them, and still renders its six charts.

## Acceptance criteria

- [ ] `grep -c StructField src/Analyse_Marche_Emploi_IA_PySpark.ipynb` prints 0.
- [ ] `task nb:check` passes (no outputs committed).
- [ ] The six charts are re-rendered on the running stack and a capture is attached to the pull request.

## Package

notebook

## Size

page

## Priority

basse

## Milestone

v0.3.0 Analysis quality

## Out of scope

- Changing the charts or the queries.

## Origin

Rewritten from: the duplication noticed in the audit of the original notebook.

## Definition of done

- [ ] `task verify` is green.
- [ ] Documentation and ADR updated where behaviour or a decision changes.
- [ ] The pull request says `Closes #n` and CI (`ci`) is green.
