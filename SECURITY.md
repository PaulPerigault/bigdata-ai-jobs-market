# Security policy

## Reporting a vulnerability

Do not open a public issue for a vulnerability. Use GitHub's
[private vulnerability reporting](https://github.com/PaulPerigault/bigdata-ai-jobs-market/security/advisories/new)
on this repository. Expect an answer within a few days.

## Scope and design choices

This is a local teaching stack, not a service. Its design choices:

- **No secret in the repository.** `.env` is ignored; `.env.example` is the only environment file
  versioned (defaults for a stack bound to the loopback interface: Postgres credentials, a Jupyter token). gitleaks scans the tree
  and the whole Git history in `task verify`, in the pre-commit hook and in CI.
- **Loopback only.** Every published port is bound to `127.0.0.1`. Do not expose the stack on a network: HDFS
  permissions are disabled (`dfs.permissions.enabled=false`) and Hive has no authentication.
- **Pinned supply chain.** Images by tag and digest, Python packages by hashes in `uv.lock`, dev tools by `tools/go.sum`,
  workflow actions by commit SHA. Nothing is downloaded at run time without a checksum.
- **Known weakness, accepted.** The Hadoop 2.7.4 and Hive 2.3.2 images are old and carry published vulnerabilities.
  They are used because the course asks for that stack; never run them on untrusted input or an exposed host.
- **No personal data.** The dataset describes job postings (titles, salaries, skills); it holds no names or contact
  details. The committed sample is synthetic.

Only the latest commit of `main` receives fixes.
