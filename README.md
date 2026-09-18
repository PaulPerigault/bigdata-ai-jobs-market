# Marché de l'emploi en IA 2025-2026 — Projet Big Data ESIEA

Projet pédagogique ESIEA (module Fondamentaux du Big Data, sujet
proposé par M. Touati Zouhaier) : construire une chaîne Big Data
complète pour analyser le marché de l'emploi en IA 2025-2026 à partir
du dataset `ai_jobs_market_2025_2026.csv` (1500 lignes, 25 colonnes).

- **Équipe** : 5 personnes, travail en parallèle sur ce dépôt.
- **Deadline** : 21/09/2026.
- **Suivi** : [`STATUS.md`](STATUS.md) (état réel du projet),
  [`JOURNAL.md`](JOURNAL.md) (journal d'exécution append-only),
  [`CLAUDE.md`](CLAUDE.md) (règles et décisions techniques détaillées),
  [Project board GitHub](https://github.com/users/PaulPerigault/projects/9).

## Architecture

```
CSV (data/raw/) → HDFS /projet_ia/raw
                 → Spark : contrôle, nettoyage, transformation
                 → HDFS /projet_ia/processed/{offres,metiers,competences}
                 → Hive (tables externes RAW + processed)
                 → Jupyter/PySpark (exploration, requêtes Hive SQL/Spark SQL, dashboard)
```

Stack orchestrée via Docker Compose (`compose.yaml` +
`compose.override.yaml`) : HDFS (namenode/datanode), Hive (metastore +
server, Postgres), Jupyter/PySpark. Détails et justification de chaque
choix d'image dans `CLAUDE.md`.

## Prérequis

- Docker + Docker Compose (Docker Desktop, ou colima sur Apple Silicon
  — voir `CLAUDE.md` pour la configuration).
- [`go-task`](https://taskfile.dev/) (`brew install go-task`).
- Python 3.12 pour les tests locaux (`pyspark==3.5.0` ne fonctionne pas
  sous Python ≥ 3.13) et Java 17 ou 21 (pas plus récent — voir
  `CLAUDE.md`, section « Tests locaux »).

## Utilisation — Taskfile

Toutes les commandes passent par `task`, seul point d'entrée documenté :

| Commande | Rôle |
|---|---|
| `task setup` | Installe les dépendances locales (pre-commit, venv de test). |
| `task up` | Démarre la stack Docker Compose (HDFS, Hive, Jupyter). |
| `task down` | Arrête la stack. |
| `task ingest` | Dépose le CSV brut dans HDFS (`/projet_ia/raw`). |
| `task etl` | Lance le pipeline Spark : nettoyage + écriture des tables `offres`/`metiers`/`competences` sur HDFS et Hive. |
| `task test` | Exécute les tests unitaires (`tests/unit/`, Spark local). |
| `task hive-shell` | Ouvre un shell Beeline connecté à HiveServer2. |
| `task jupyter` | Affiche l'URL du notebook Jupyter/PySpark. |
| `task report` | Compile le rapport LaTeX (`report/main.tex`) via Docker, sans dépendance LaTeX locale. |
| `task screenshots-cli` | Régénère les captures de commandes CLI (Hive/Spark) pour le rapport. |
| `task screenshots-web` | Régénère les captures d'interfaces web (HDFS NameNode, Jupyter) pour le rapport. |
| `task lint` | Lance `pre-commit run --all-files` (ruff, sqlfluff, gitleaks). |

Workflow type de bout en bout :

```bash
task up          # démarre la stack, attend que les 6 services soient healthy
task ingest      # CSV -> HDFS /projet_ia/raw
task etl         # Spark : nettoyage + tables offres/metiers/competences -> HDFS + Hive
task hive-shell  # requêtes Hive SQL (sql/hive/*.sql)
task jupyter      # notebook Jupyter/PySpark (requêtes Spark SQL, dashboard)
task report       # compile le rapport PDF
```

## Structure du dépôt

```
compose.yaml, compose.override.yaml   # stack Docker (services de base + overrides dev)
Taskfile.yml                          # point d'entrée des commandes
scripts/                              # ingestion HDFS, captures d'écran
sql/hive/                             # DDL RAW, requêtes d'analyse, KPI
src/etl/                              # schéma, nettoyage, construction des tables (Spark)
src/etl_pipeline.py                   # point d'entrée task etl (spark-submit)
src/*.ipynb                           # notebook Jupyter/PySpark (exploration, dashboard)
tests/unit/                           # sanity checks Spark local (pytest)
report/                               # rapport LaTeX modulaire (main.tex + preamble/ + chapters/)
data/raw/                             # CSV brut (gitignored, jamais commité)
```

## Modèle de données

Trois tables construites par le pipeline ETL et exposées dans Hive
(base `processed`) :

- **`offres`** : une ligne par offre d'emploi (`job_id`, `metier_id`
  FK, salaire, expérience, localisation, etc.).
- **`metiers`** : une ligne par `job_title` distinct (`metier_id` en
  hash déterministe `sha2(job_title, 256)`, pas d'ID auto-incrémenté
  instable).
- **`competences`** : une ligne par couple `job_id`/compétence, issue
  de l'explosion de `required_skills`.

Détails et chiffres réels dans `report/chapters/07_construction_tables.tex`.

## Rapport

Le rapport final (LaTeX, couleurs ESIEA) vit dans `report/` :
`main.tex` + `preamble/` (charte graphique) + `chapters/` (un fichier
par chapitre). Compilation via `task report` (XeLaTeX dans un conteneur
Docker pinné, aucune dépendance LaTeX locale requise).

## Conventions de contribution

- Commits [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- `pre-commit run --all-files` obligatoire avant tout push (ruff,
  sqlfluff, gitleaks) — jamais un run scopé aux fichiers touchés.
- Transformations Spark versionnées en scripts `.py` dans `src/etl/`,
  pas seulement écrites dans le notebook.
- Voir `CLAUDE.md` pour l'ensemble des règles et décisions techniques
  détaillées (images Docker pinnées, choix d'architecture, bugs
  rencontrés et corrigés).
