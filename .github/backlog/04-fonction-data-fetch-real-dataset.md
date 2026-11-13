---
title: "feat(data): document a checksum-verified way to fetch the real dataset"
labels: ["type:fonction", "pkg:data", "prio:normale", "taille:page"]
milestone: "v0.2.0 Reproducible local run"
assignee: PaulPerigault
---

## Context

The real dataset is downloaded by hand from Kaggle and checked afterwards by `task data:raw:check`. A fetch step would remove the manual work, but Kaggle needs an account and a token, and the repository must not handle that secret.

## Goal

A documented, optional way to obtain the file that never stores a token in the repository and ends on `task data:raw:check`.

## Acceptance criteria

- [ ] `data/README.md` describes the procedure with the Kaggle CLI version pinned.
- [ ] No token or credential file is added to the repository or required by CI.
- [ ] `task data:raw:check` stays the gate before `task ingest`.

## Package

data

## Size

page

## Priority

normale

## Milestone

v0.2.0 Reproducible local run

## Out of scope

- Redistributing the file.
- Running the fetch in CI.

## Origin

Rewritten from: step 2 of the original onboarding.

## Definition of done

- [ ] `task verify` is green.
- [ ] Documentation and ADR updated where behaviour or a decision changes.
- [ ] The pull request says `Closes #n` and CI (`ci`) is green.
