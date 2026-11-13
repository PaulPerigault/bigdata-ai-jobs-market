# 0002. A synthetic sample instead of the dataset

- **Status:** accepted
- **Date:** 2026-11-13

## Context

The pipeline runs on a Kaggle dataset (1500 rows, 383 900 bytes). Its public page does not state a licence (read on
2026-11-13), so redistribution is not clearly allowed. The original repository never committed the file (`data/raw/`
was ignored), but one branch of its history did. The tests and `task demo` need data that works offline.

## Decision

- The real file is not committed. `task data:raw:check` verifies a local copy by SHA-256, size and line count;
  `data/README.md` documents source, licence status and how to obtain it.
- A seeded generator (`data/gen_sample.py`) writes 60 invented rows with the same 25 columns to `data/sample/`.
  `task data:check` replays it and fails on drift. Tests and `task demo` use it.
- Reopen the question when the licence is clarified (issue in the backlog): a clear permissive licence would allow a
  checksum-verified download task or a real sample.

## Consequences

- Anyone can run the tests and the demo offline. The figures of the report cannot be reproduced without the real file.
- The sample proves the plumbing, not the analysis: its statistics mean nothing.

## Alternatives rejected

- Commit the real CSV (384 KB): small, but a licence risk on a public repository for no gain in testing.
- Commit a 50-row excerpt of the real file: still redistribution of part of it, and the licence is unknown.
- Download from Kaggle in a task: needs an account and a token, and the repository must not handle that secret.

## Main risk and mitigation

Risk: the generator drifts from the real schema. Mitigation: `tests/unit/test_sample_data.py` compares the sample header with
`RAW_SCHEMA`, and the smoke test runs the real cleaning and table code on it.
