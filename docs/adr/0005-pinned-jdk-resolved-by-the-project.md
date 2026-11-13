# 0005. The project resolves its own JDK for the Spark tests

- **Status:** accepted
- **Date:** 2026-11-13

## Context

[ADR 0003](0003-java-and-python-pins-for-spark-tests.md) fixed the versions (Java 11 or 17) but left the JDK to the
machine: with another Java, `task verify` skipped the 12 Spark tests. A skip is honest but it lets a local run pass
without testing the part that matters. During the rebuild a Temurin 17 had to be downloaded by hand into a scratch
directory.

## Decision

- `dev/jdk` (Go, standard library only) prints a `JAVA_HOME`. Order: a valid JDK 11 or 17 already in `JAVA_HOME`; the
  cache `.tools/jdk` (ignored by Git); a download of Eclipse Temurin 17.0.21+9 for the current OS and CPU.
- The archive is pinned by URL, size and **SHA-256** in the source. The digest is checked while the file is written,
  and nothing is extracted before it matches. Extraction refuses paths that leave the target and skips links.
- `task jdk` prints it; `task test` sets `JAVA_HOME` from it and `REQUIRE_SPARK=1`. `task verify` runs `task test`, so
  the 12 Spark tests run or the task fails.
- No binary is committed. Supported pins: Windows x64, Linux x64 and arm64, macOS x64 and arm64.

## Consequences

- First `task test` downloads about 190 MB (once). Offline, with no valid JDK, it fails with the reason instead of
  skipping.
- Refreshing the JDK means changing URL, size and digest together in `dev/jdk/resolve.go`, after reading the release
  notes. The unit tests cover the reuse of an environment JDK, the digest check, the size cap and path traversal,
  without network.
- `uv run pytest` by hand keeps the loud skip of ADR 0003.

## Alternatives rejected

- Download with a script: scripts are not allowed here; a typed, tested Go program is.
- `actions/setup-java` locally: CI only. CI keeps using it, pinned by commit SHA.
- Trust the Java on the PATH: the failure that ADR 0003 records (Java 22).

## Main risk and mitigation

Risk: a compromised release host serves a different archive. Mitigation: the SHA-256 is in the source, reviewed with
the code; a mismatch aborts before extraction (tested).
