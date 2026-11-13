---
title: "decision(data): confirm the dataset licence and the redistribution policy"
labels: ["type:decision", "pkg:data", "prio:normale", "taille:trait", "etat:a-valider"]
milestone: "v0.2.0 Reproducible local run"
assignee: PaulPerigault
---

## Context

ADR 0002 keeps the real file out of the repository because the public page does not state a licence (read on 2026-11-13). The author of the dataset may have stated one elsewhere, or can be asked.

## Goal

The licence is known, or the repository records that it cannot be known, and ADR 0002 is updated accordingly.

## Acceptance criteria

- [ ] The source page and any licence file are read and quoted with the date.
- [ ] ADR 0002 is updated (status, consequences) or a new ADR supersedes it.
- [ ] If redistribution is allowed, a follow-up issue adds a checksum-verified download.

## Package

data

## Size

trait

## Priority

normale

## Milestone

v0.2.0 Reproducible local run

## Out of scope

- Committing the file in this issue.

## Origin

Rewritten from: the open question of ADR 0002.

## Definition of done

- [ ] `task verify` is green.
- [ ] Documentation and ADR updated where behaviour or a decision changes.
- [ ] The pull request says `Closes #n` and CI (`ci`) is green.
