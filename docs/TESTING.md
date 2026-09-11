# Politique de tests

Approche pragmatique en 3 niveaux. Objectif : attraper les régressions sur la
logique de transformation et la qualité des données, sans faire dépendre la
CI d'un cluster k3d complet (trop lent/coûteux pour la valeur apportée sur ce
projet, à durée de vie courte).

## Niveau 0 — déjà couvert (pre-commit / CI existants)

Pas des "tests" à proprement parler, mais le premier filet : lint (`ruff`,
`yamllint`), détection de secrets, validation de manifests (`kubeconform`),
scan de vulnérabilités (`Trivy`). Voir `.pre-commit-config.yaml` et
`.github/workflows/ci.yml`.

## Niveau 1 — tests unitaires (obligatoire)

Les fonctions de transformation PySpark (nettoyage, construction des 3
tables, `split`/`explode` des compétences) doivent être extraites en
fonctions pures et testables — pas de logique métier directement dans le
`spark-submit` du script principal.

- Framework : `pytest` + une `SparkSession` locale (fixture `session-scoped`,
  `master("local[1]")`)
- Fixtures : petits DataFrames construits à la main (5-10 lignes), jamais le
  CSV complet
- Couverture minimale attendue :
  - règles de nettoyage (nulls, doublons, types) sur des cas limites
  - stabilité de `metier_id` (même métier → même id à chaque exécution)
  - `split()`/`explode()` de `required_skills` (compte de lignes correct,
    pas de compétence vide)
- Emplacement : `tests/unit/`

## Niveau 2 — tests de qualité de données (obligatoire, exécution manuelle)

Assertions sur les 3 tables une fois écrites dans `/processed`. Ne tournent
**pas** en CI (nécessitent le cluster) — exécutés manuellement après un
`task k3d:up` + pipeline, via `task test:data`.

- `offres` : `job_id` unique, `salary_min_usd <= salary_max_usd`,
  `country`/`job_title` non nuls
- `metiers` : `metier_id` unique
- `competences` : tout `job_id` référencé existe dans `offres` (intégrité
  référentielle), aucune compétence vide après split
- Emplacement : `tests/data_quality/`

## Niveau 3 — vérification manuelle (hors CI, hors pytest)

- Zeppelin/DAS : checklist de vérification visuelle des 6+ visualisations
  (titre, requête identifiable, interprétation) — voir
  `docs/trame-rapport.md`
- Voilà : lancement local (`voila voila-app/dashboard.ipynb`), vérification
  que le dashboard se charge sans erreur

## Explicitement hors scope

- Pas de test d'intégration qui déploie HDFS/Hive/Spark/Zeppelin en CI
- Pas de test end-to-end automatisé sur le cluster k3d
- Ces vérifications restent manuelles, documentées dans une checklist plutôt
  qu'automatisées — rapport coût/bénéfice défavorable vu le délai et la durée
  de vie du cluster (jetable)

## CI

Un job `test` tourne sur chaque PR/push : `pytest tests/unit/ -v`. Le job
échoue si un test unitaire échoue ; les tests de qualité de données restent
manuels (niveau 2) et ne bloquent pas la CI.
