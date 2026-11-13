# Contributing

Thanks for looking. This is a small project with a strict method; the rules are written once in
[AGENTS.md](AGENTS.md) and checked by CI.

## Set up

```bash
git clone https://github.com/PaulPerigault/bigdata-ai-jobs-market.git
cd bigdata-ai-jobs-market
pip install uv==0.13.8
go install github.com/go-task/task/v3/cmd/task@latest   # or: go tool -modfile=tools/go.mod task
task setup     # locked Python environment, .env, pinned tools, Git hooks (Lefthook)
task verify    # everything CI runs
```

You need Go (dev tools), Python 3.11 and uv, and Java 11 or 17 (`JAVA_HOME`) for the Spark tests. On Windows, Git for
Windows provides the POSIX tools some targets use. Docker is only needed for the stack (`task demo`).

## Workflow

1. One issue per change, created from a form (`.github/ISSUE_TEMPLATE/`), with labels, a milestone and
   acceptance criteria. Blank issues are disabled.
2. Branch `<type>/<issue>-<slug>`, for example `feat/42-schema-validation`.
3. Commits follow Conventional Commits: `type(scope): lower-case subject`, 72 characters at most,
   types `feat fix docs style refactor test chore ci perf revert`. No tool signature
   (`Co-authored-by`, "Generated with"). The `commit-msg` hook checks it.
4. Open a PR to `main` with `Closes #n`. CI must be green (`ci` is the required check). Merge is squash.
5. `task verify` passes locally before you push: it is the `pre-push` hook.

## What a good change looks like

- A test for each behaviour, table-driven where it fits, on tiny synthetic data. Tests never use the public network
  and never need HDFS or Hive.
- Spark transformations live in `src/etl/`, not only in the notebook. Notebook outputs are never committed.
- Pins stay pins: no `latest` image, no unpinned package, no action by tag. Refresh digests and hashes deliberately.
- Docs move with the code: `task check:docs` fails if a documented task, path or relative link is gone.

## Security

Never open an issue for a vulnerability: see [SECURITY.md](SECURITY.md). Do not add keys, tokens or
personal data to the repository, including in tests; use `data/sample/`.
