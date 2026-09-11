# Conventions du projet

## Branches

Format : `<type>/<scope>-<description-courte>`

Types :
- `feat` — nouvelle fonctionnalité (pipeline, dashboard, interface)
- `infra` — infrastructure k3d/k8s
- `fix` — correction de bug
- `docs` — documentation / rapport
- `security` — durcissement, secrets, network policies
- `chore` — maintenance, dépendances

Scopes usuels : `hdfs`, `hive`, `spark`, `zeppelin`, `voila`, `k3d`, `ci`, `report`

Exemples :
- `infra/k3d-bootstrap`
- `feat/spark-cleaning-job`
- `feat/table-competences-explode`
- `docs/architecture-diagram`
- `security/networkpolicies-bigdata`

## Commits (Conventional Commits)

Format : `<type>(<scope>): <description>`

Types : `feat`, `fix`, `infra`, `docs`, `security`, `chore`, `test`

Exemples :
- `feat(spark): add explode transformation for required_skills`
- `infra(k3d): deploy hive metastore statefulset`
- `docs(report): rédaction section 9 analyse salaires`

## Labels

**Type**
- `type:feature`
- `type:bug`
- `type:infra`
- `type:docs`
- `type:security`
- `type:chore`

**Scope**
- `scope:hdfs`
- `scope:hive`
- `scope:spark`
- `scope:zeppelin`
- `scope:voila`
- `scope:k3d`
- `scope:ci`
- `scope:report`

**Priorité**
- `priority:p0` — bloquant, deadline en jeu
- `priority:p1` — important
- `priority:p2` — normal
- `priority:p3` — nice to have

**Statut académique**
- `academic:required` — nécessaire pour la note
- `academic:bonus` — au-delà du barème

**Équipe** (voir `docs/team-roles.md`)
- `team:infra`
- `team:data-eng`
- `team:analytics`
- `team:insights`
- `team:docs-qa`

## Workflow issue → branche → PR

1. Une tâche = une issue (voir `docs/issues-seed.yml`)
2. `gh issue develop <numéro> --checkout` pour créer la branche liée à
   l'issue (nom conforme aux conventions ci-dessus)
3. Travailler sur la branche, committer (Conventional Commits)
4. Ouvrir une PR qui `Closes #<numéro>` — pas de push direct sur `main`
   (protection de branche : PR obligatoire + CI verte)

## Pull Requests

- Une PR = une issue liée (`Closes #N`)
- Pas de merge sans que le scan CI (lint + Trivy + tests) soit vert
- Description courte : quoi + pourquoi, pas de pavé
