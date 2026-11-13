# 0003. Java and Python pins for the Spark tests

- **Status:** accepted
- **Date:** 2026-11-13

## Context

`pyspark==3.5.0` matches the `jupyter/pyspark-notebook:spark-3.5.0` image used by the stack. On the rebuild machine
(Windows 11) two combinations failed and one worked:

- Java 22 with PySpark 3.5.0: the Spark session does not start.
- Java 17 with CPython 3.12: the session starts, but every task that uses a Python worker fails with
  `Python worker exited unexpectedly (crashed)` (7 of 12 tests). The cause was not investigated.
- Java 17 (Temurin 17.0.21) with CPython 3.11: 12 of 12 tests pass.

The Jupyter image itself runs Python 3.11.

## Decision

- `.python-version` is 3.11 and `requires-python` is `>=3.11,<3.12`.
- The `spark` fixture skips when the JVM it would use (`JAVA_HOME`, else `PATH`) is not Java 11 or 17, with the reason in the
  report. `REQUIRE_SPARK=1`, set by CI, turns the skip into a failure, so CI cannot pass without running Spark.
- CI uses Java 17 (Temurin) and Python 3.11.

## Consequences

- A machine with another Java still runs `task verify`, with the Spark tests reported as skipped: it cannot silently
  replace the CI result. The README states the Java requirement.
- Moving to Spark 4 (Java 17 or 21, Python 3.9 or later) is a separate milestone (v0.4.0), together with the images.

## Addendum, 2026-11-13

The JDK is no longer left to the machine: `task test` resolves a JDK 17 with `dev/jdk` and sets `REQUIRE_SPARK=1`, so a
local `task verify` runs the Spark tests or fails ([ADR 0005](0005-pinned-jdk-resolved-by-the-project.md)). The skip
remains only for a bare `uv run pytest`.

## Addendum, 2026-11-13 (security patch release)

`pyspark` moves from 3.5.0 to 3.5.8, the last patch of the 3.5 line, to close advisories GHSA-9437-39hj-3c93 (fixed in
3.5.8) and GHSA-6p6v-m64v-jx8q (fixed in 3.5.2). No move to 4.x is needed, so this ADR holds. The test client (3.5.8) is
now newer than the Spark of the Compose images (3.5.0), which only run the stack and do not use the Python wheel pinned
here; the 12 Spark tests pass on 3.5.8. `.github/dependabot.yml` ignores `pyspark` updates outside 3.5.x, so a 4.x
proposal is never opened again.

## Alternatives rejected

- Run the tests in the Jupyter container only: needs a Docker daemon for every test run, slower, and absent here.
- Silent skip without `REQUIRE_SPARK`: a green CI that tested nothing.

## Main risk and mitigation

Risk: the skip hides a broken environment on a developer machine. Mitigation: the skip reason is printed (`-ra`), the pre-push
`task verify` shows it, and CI fails instead of skipping.
