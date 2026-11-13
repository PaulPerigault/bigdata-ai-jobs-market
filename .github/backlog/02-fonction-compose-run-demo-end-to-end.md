---
title: "feat(compose): run task demo end to end and record the result"
labels: ["type:fonction", "pkg:compose", "prio:haute", "taille:page"]
milestone: "v0.2.0 Reproducible local run"
assignee: PaulPerigault
---

## Context

The stack ran on the original authors' machines in September 2026, but the rebuilt `compose.yaml` (digests, `platform`, override file) and the new `task demo` have not been run: no Docker daemon was available during the rebuild.

## Goal

`task demo` goes from a clean Docker state to a Hive count on the synthetic sample, on at least one Linux machine and one Apple Silicon machine, with timings and memory noted.

## Acceptance criteria

- [ ] `task up` reports six healthy services within 10 minutes on a clean state.
- [ ] `task demo` ends with `SELECT COUNT(*) AS offres FROM processed.offres` returning 60.
- [ ] The README Limits section states the machines and the date of the run.
- [ ] Any fix needed (ports, healthchecks, memory limits) is committed with an explanation in `docs/journal/`.

## Package

compose

## Size

page

## Priority

haute

## Milestone

v0.2.0 Reproducible local run

## Out of scope

- Upgrading any image (see the v0.4.0 issues).
- Running the real dataset.

## Origin

Rewritten from: the stack validation notes of the original project.

## Definition of done

- [ ] `task verify` is green.
- [ ] Documentation and ADR updated where behaviour or a decision changes.
- [ ] The pull request says `Closes #n` and CI (`ci`) is green.
