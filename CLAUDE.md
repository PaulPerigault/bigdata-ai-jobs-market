@AGENTS.md

# Claude Code notes

- Start with `task test` to know the baseline, finish with `task verify` (it includes `skills:verify`). Spark tests need
  a Java 11 or 17, resolved for you by `task jdk` (ADR 0005); on Windows, Python 3.11 (see ADR 0003).
- The skills of `.claude/skills/` are copies of the workspace catalogue: never edit them here.
- Begin every industrialization with the Context phase (period, origin, motivation, what changed), then fill
  the README `Context` section.
- Writes to GitHub for publication go only through the workspace tool `repoflow`, run by Task from the workspace
  (the `publish:*` targets with `REPO=<name>`); never by hand, never by a script. The workspace
  `publish-config\publish-policy.json` says which repositories and steps are allowed.
- `.claude/settings.json` denies the risky commands; a denial is a stop, not an obstacle to route around.
- No tool signature in commits or pull requests (the settings leave `attribution` empty).
