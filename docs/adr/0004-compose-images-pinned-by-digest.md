# 0004. Compose images pinned by digest, old stack kept

- **Status:** accepted
- **Date:** 2026-11-13

## Context

The stack uses `bde2020` Hadoop 2.7.4 and Hive 2.3.2 images (amd64 only, unmaintained), `postgres:13.18` and
`jupyter/pyspark-notebook:spark-3.5.0`. A tag can move; the original files pinned tags only. The course asks for HDFS and Hive.

## Decision

- Every `image:` of `compose.yaml` carries its tag and its digest, resolved on 2026-11-13 from the registry manifest
  (multi-arch index digest for `postgres` and `jupyter`, the single manifest for the amd64-only `bde2020` images).
  `task compose:check` fails on any image without `@sha256:`.
- The `bde2020` services declare `platform: linux/amd64` so that Docker emulates them on Apple Silicon.
- The old versions are kept: moving to a maintained Hadoop 3 and Hive 4 set is a separate piece of work (milestone v0.4.0).
- The report is built in `texlive/texlive:TL2025-historic` pinned by digest as well.

## Consequences

- Builds are reproducible; a refresh is a deliberate act (resolve the new digest, run the demo).
- Dependabot (`docker-compose` ecosystem) proposes digest updates; the old `bde2020` images will never have one.
- The images keep their published vulnerabilities (see `SECURITY.md`): acceptable for a loopback-only teaching stack, not for more.

## Alternatives rejected

- Keep tags only: not reproducible.
- Build own images: more code to maintain for a coursework repository.

## Main risk and mitigation

Risk: a digest points to an image that the registry later removes. Mitigation: the tag stays next to the digest, so the
intent is readable and a re-resolution is possible.
