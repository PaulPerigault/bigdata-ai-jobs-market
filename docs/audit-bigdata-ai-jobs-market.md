# Audit of the original repository (2026-11-13)

Scope: the read-only clone of the original repository, **all four branches and the whole history** (49 commits), plus the
tree of the default branch that this rebuild starts from. No value found (secret, e-mail, name) is written here: the
audit gives counts, files and categories. The real names are kept in the owner's private notes, outside any repository.

## Method

| Check | How |
| --- | --- |
| Secrets | gitleaks 8.x on the whole history, all branches, redacted; each finding triaged by hand |
| People, e-mails, handles | `git grep` (case-insensitive) on every revision, plus author and committer metadata of every commit |
| Tool trailers | trailer lines of every commit message |
| Machine paths, school forge | patterns for Windows, macOS and WSL home paths, forge hostnames |
| Datasets | history of the CSV path, size, schema read, personal-data review |
| Notebook outputs | JSON of the notebook: cells with outputs and execution counts |
| IDE and agent files | list of tracked paths on every branch |
| Report figures | all 20 screenshots opened and read (2026-11-13, second pass): generated terminal frames, a Jupyter page, the HDFS browser, seaborn charts. No name, e-mail, handle, token, internal URL or personal path; none removed |
| Report text | scanned with the forbidden patterns (0 hit) and a "First Last" heuristic; cover, chapters 1, 13, 14, 15 and the end of chapter 3 read in full, the other chapters not read line by line |

Not read: the old `.env.example`. A deny rule of this workspace refuses reads and edits of `.env*` files, and the rule was
respected. The file was checked only by a count-only pattern search (access tokens, key headers, long base64-like strings,
e-mail shapes, IPv4 addresses: 0 match) and by gitleaks on the tree (0). That cannot show that the file holds no name or
personal value in another shape: this limit stands.

## Findings

| # | Finding | Where | Severity | Action |
| --- | --- | --- | --- | --- |
| 1 | Course supervisor named | default branch: 10 occurrences on 6 lines in 5 files (README, agent notes, report title page, introduction, architecture chapter); 5 lines on each report branch; 2 on the infrastructure branch | privacy | replaced by "the course supervisor" everywhere |
| 2 | Teammates named (four people, first names and surnames) | report branches only: the cover page of the report (8 lines per branch) | privacy | not in the default-branch tree; never copied; patterns forbid them in the clean repository |
| 3 | Teammate's personal e-mail domain and handle | author and committer metadata of 7 commits on the report branches; domain also in the report branches' journal | privacy | history not republished; patterns forbid the domain and the handle |
| 4 | Machine paths of a teammate (WSL path with a Windows user name) | report branches: 4 lines in the journal | privacy | not in the default branch; patterns forbid the path shapes |
| 5 | Tool trailers: 32 `Co-authored-by` lines naming an AI tool | commit messages, all on the default branch | policy | history not republished; commit-msg hook and the clean proof refuse any signature |
| 6 | 13 `Co-authored-by` lines naming one author's former handle and personal e-mail | commit messages, default branch | privacy | history not republished; patterns forbid the handle and the personal e-mail provider |
| 7 | Two author identities for the owner: one with a personal e-mail, one noreply | 36 commits of the default branch (23 and 13) | privacy | the clean repository has one commit with the noreply identity |
| 8 | Secret scan: 2 findings (`generic-api-key`) | infrastructure branch, `.secrets.baseline`, commit of 2026-09-11 | none after triage | **false positives**: the file is a detect-secrets baseline; the matched lines are `hashed_secret` entries of type "Hex High Entropy String" with `is_verified: false`, recorded for a Dockerfile of that branch (hashes of pinned download checksums). No real secret, nothing to revoke. Not republished anyway |
| 9 | Full dataset committed in history | CSV (383 900 bytes, 1500 rows) in the first commit and the infrastructure branch, removed from the default branch | licence | licence not stated by the source (ADR 0002); not committed in the rebuild |
| 10 | Notebook with outputs | 7 of 13 code cells had outputs, 6 of them embedded PNG images in base64 (360 KB file). A loose key-shaped search matched inside that base64 data; the strict AWS key-id pattern (`AKIA` plus 16 characters) has 0 hits | hygiene, false positive | `nbstripout`: 30 KB, checked by `task nb:check` |
| 11 | IDE files | `.idea/` (3 files) and `.vscode/` (2 files) on the default branch | hygiene | deleted, ignored |
| 12 | Agent graph output | 4 files (about 400 KB: graph JSON and HTML, report, manifest) on the report branches | hygiene | not in the default branch; ignored, forbidden by pattern |
| 13 | Agent instruction file mixing team rules, deadlines and decision history (32 KB), journal and status files (32 KB and 35 KB) | default branch | hygiene | replaced by `AGENTS.md`; the useful technical decisions are kept in `docs/project-notes.md`; journals kept in the owner's private notes |
| 14 | A script that mounts the Docker socket into a wrapper container (`./run`) | default branch | security | removed; `task` is pinned by `tools/go.sum` instead |
| 15 | Action tags not pinned, images by tag only | CI and Compose | supply chain | actions by SHA, images by digest |

Not found: API keys, tokens, private keys, passwords other than the documented local defaults (Postgres and Jupyter on
the loopback interface), personal data in the dataset (job titles, categories, cities, countries, salary ranges, skills),
Zeppelin or other abandoned components in the tree.

## Datasets

| Item | Value |
| --- | --- |
| File | `ai_jobs_market_2025_2026.csv`, 1500 rows, 25 columns, 383 900 bytes |
| SHA-256 | `6ae7bc7bf724250cd8c977f86b620128318070a23cb0b17340e58d2321f7864e` |
| Source | Kaggle, "AI Jobs Market 2025-2026 \| Salaries" |
| Licence | not stated on the public page (read 2026-11-13); not verified elsewhere |
| Personal data | none by schema; values not individually reviewed |
| Decision | not redistributed; a seeded synthetic sample replaces it in tests and in the demo |

## Patterns to forbid in the clean repository

Written in `publish-config/bigdata-ai-jobs-market.forbidden.txt` (outside the repository). Categories:

1. the course supervisor's first and last name;
2. the four teammates' first names and surnames, with accent variants;
3. the teammate's handle and e-mail domain;
4. the owner's former handle and personal e-mail provider (only the noreply identity is allowed);
5. the school forge host, WSL, macOS and Windows home paths;
6. editor and agent directories (outside `.gitignore` and `docs/`);
7. tool trailers and signatures, personal e-mail providers, private IPv4 addresses;
8. credential shapes (GitHub tokens, cloud access key ids, private key headers).

## After the rebuild

- The report (French) keeps the school branding and the course name; the supervisor is "the course supervisor".
- The README *Context* states the period, the origin and the owner's contribution without attributing others' work.
- The publication steps (rename of the public original to a private legacy repository, then the new repository) are not run
  by this rebuild.
