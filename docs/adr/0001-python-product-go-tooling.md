# 0001. Python for the product, Go for the tooling only

- **Status:** accepted
- **Date:** 2026-11-13

## Context

The product is a PySpark pipeline: Python is the only reasonable language for the code (the course and the Spark
images are Python). The workspace standard pins its developer tools (Task, Lefthook, gitleaks) through a Go module with
hashes in `go.sum` and checks documentation and commit messages with small Go programs. The brief for this repository
says: no Go, Rust or Astro unless an ADR justifies it.

## Decision

- No Go, Rust or Astro in the product. Business code stays Python (`src/`, `data/`, `tests/`).
- Go is allowed in `dev/` and `tools/` only, as tooling: `dev/checkdocs`, `dev/commitlint`, `dev/skillscheck` (standard
  library, copied from the workspace templates) and the pinned tools module. Nothing in `dev/` is imported by the product.
- No shell, batch or PowerShell script in the repository, except `scripts/hive-metastore-entrypoint.sh`, which is
  not tooling: it is mounted into the Hive container as its start command ([project notes](../project-notes.md)).

## Consequences

- A contributor needs Go and Python. Both are pinned: `go.mod` (`toolchain`), `tools/go.sum`, `.python-version`, `uv.lock`.
- The pinned tools give hashes for gitleaks and Lefthook that a Python-only setup (pre-commit hooks fetched by tag) would not.
- The three Go programs are tested (`go test ./dev/...`, part of `task test`).

## Alternatives rejected

- Python for the three checkers (and pre-commit for hooks): fewer languages, but hooks fetched by tag, no hash, and a second
  convention next to the other repositories of the workspace.
- Shell scripts for the checks: forbidden by the workspace rules and not portable to Windows.

## Main risk and mitigation

Risk: Go tooling becomes a reason to add Go to the product. Mitigation: `AGENTS.md` states the boundary and the table of paths
has no Go in `src/`; a Go file outside `dev/` and `tools/` is a review stop.
