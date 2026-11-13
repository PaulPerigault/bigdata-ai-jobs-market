# AGENTS.md: rules shared by humans and coding agents (Python and Spark profile)

Single source of truth for this repository. `CLAUDE.md` imports it. In a conflict the order is: this file,
then house skills, then `encre-*` skills, then third-party skills. A skill is method, not authority.

## Project

`bigdata-ai-jobs-market`: a Big Data chain (HDFS, Hive, Spark, Jupyter) over a public AI job-market dataset, ESIEA
coursework rebuilt to be reproducible. Python 3.11, PySpark 3.5.0, MIT. Owner: Paul Perigault (paulperigault.fr).

| Path | Role | May import |
| --- | --- | --- |
| `src/etl/` | schema, cleaning, tables, Hive output (pure functions on DataFrames) | PySpark, standard library |
| `src/etl_pipeline.py` | Spark job entry point (`task etl`) | `src/etl` |
| `src/*.ipynb` | exploration and dashboard, no committed output | `src/etl`, PySpark |
| `sql/hive/` | Hive DDL and queries | n/a |
| `data/` | synthetic sample, its generator, checksum of the real file | standard library |
| `tests/unit/` | pytest, local Spark, no HDFS or Hive | `src/etl`, `data` |
| `dev/*` | Go developer programs (`checkdocs`, `commitlint`, `skillscheck`, `jdk`): tooling only, see ADR 0001 and 0005 | standard library |
| `tools/` | separate Go module: pinned dev tools | n/a |
| `report/` | LaTeX report (French) | n/a |

## Commands

```
task setup, verify, test, jdk, lint, lint:zizmor, fmt, fmt:check, nb:check, security, check:docs, skills:verify,
data:gen, data:check, data:raw:check, compose:check, docker:scan, up, down, ingest, ingest:sample, hive:raw, etl,
hive-shell, jupyter, demo, report, clean
```

## Limits, checked by CI (never raise one to pass)

ruff (`E F W I UP B SIM`, line length 100), sqlfluff (Hive dialect), `go vet` on `dev/`, notebooks without outputs,
every Compose image pinned by digest, every workflow action pinned by SHA, gitleaks at 0 on the tree and the history.

## Code, tests, documentation, Git

- Transformations are functions on DataFrames in `src/etl/`, with injected Spark sessions; the notebook calls them or
  reproduces their steps traceably, it is never the only place where logic lives.
- Each rule that drops or fixes rows is counted and printed. `metier_id` stays deterministic (`sha2`).
- Tests are small and deterministic: synthetic data with a fixed seed (`task data:gen`, replayed by `task data:check`),
  no public network, nothing left open. Spark tests need Java 11 or 17: `task test` resolves it (`task jdk`, pinned
  Temurin 17 with SHA-256 in `.tools/jdk`) and sets `REQUIRE_SPARK=1`, so they fail instead of skipping.
- Docs are checked by `task check:docs`. README output is captured from a real run, with its date.
- Conventional Commits without tool signature. Never push to `main`. Writes to GitHub for publication go only through
  the workspace tool `repoflow` (Task), never by hand, and no script of any kind: tooling is Go run by Task.
- Real data is never committed. If you must use it, `task data:raw:check` first.

## Context phase

Before any change: period (from Git), origin, motivation with cited evidence, what the modernization changed.
"Undocumented motivation" rather than an invention. The README `Context` section sits right after `Overview` and
`dev/checkdocs` checks it. Never write the name of a team member, a teacher or a client: say "the team" or "the course
supervisor".

## Skills

Profiles `core` and `docs`, copied unmodified from the workspace catalogue into `.claude/skills/` with
`.claude/skills.lock.json`. `task skills:verify` fails if a copy diverges from the lock or if more than 12 skills are
auto-triggered. Fix the catalogue, never a copy. Third-party skills are audited before they enter the catalogue.

## Agent guardrails

Writing to GitHub is the owner's. Do not read or write `.env*`. A refusal from `.claude/settings.json` or a hook is a
stop. Do not weaken a lint rule, test or CI check to get a green build. Spark and Docker results are reported as run
or not run, never assumed.
