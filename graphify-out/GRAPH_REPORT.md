# Graph Report - bigdata-ai-jobs-market  (2026-09-28)

## Corpus Check
- 43 files · ~82,590 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 39 file(s) not represented in the graph (top: .tex 22, (none) 5, .ttf 5)

## Summary
- 252 nodes · 258 edges · 51 communities (22 shown, 29 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 34 edges (avg confidence: 0.81)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `58674e3a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- internal task log
- pyspark_sql
- src/etl_pipeline.py (task etl, spark-submit)
- Images Docker pinnées (jamais :latest)
- État actuel — ce qui est FAIT et vérifié
- src/etl/tables.py
- screenshots_web.py
- Rapport LaTeX modulaire (main.tex + preamble/ + chapters/)
- ./run wrapper go-task containerisé
- task screenshots-cli (freeze)
- gitleaks hook
- pre-commit run --all-files obligatoire avant push
- Règles d'usage graphify (AGENTS.md)
- screenshots_cli.sh
- Tâche infra issue template
- Périmètre de sécurité du projet
- yamllint hook
- run
- 01_ingest_hdfs.sh
- sql/hive/00_create_raw_table.sql
- Conventional Commits
- bigdata-ai-jobs-market
- check-added-large-files hook
- check-merge-conflict hook
- check-yaml hook
- end-of-file-fixer hook
- mixed-line-ending hook
- ruff-format hook
- ruff hook
- sqlfluff-lint hook
- trailing-whitespace hook
- Bind des ports sur 127.0.0.1 (jamais 0.0.0.0)
- scripts/etl_pipeline.py
- src/etl_pipeline.py
- scripts/etl/tables.py
- test_tables.py
- scripts/etl/cleaning.py
- src/etl/cleaning.py
- Livrable final — Projet Big Data : Marché de l'emploi en IA 2025-2026
- test_row_counts.py
- test_cleaning.py
- pyspark_sql_types
- delivery/sql/hive/00_create_raw_table.sql

## God Nodes (most connected - your core abstractions)
1. `internal task log` - 8 edges
2. `Rapport LaTeX modulaire (main.tex + preamble/ + chapters/)` - 8 edges
3. `namenode service` - 7 edges
4. `src/etl_pipeline.py (task etl, spark-submit)` - 7 edges
5. `Images Docker pinnées (jamais :latest)` - 7 edges
6. `jupyter service` - 6 edges
7. `metier_id déterministe sha2(job_title,256)` - 6 edges
8. `./run wrapper go-task containerisé` - 6 edges
9. `write_processed_table()` - 5 edges
10. `write_processed_table()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Test à blanc de l'onboarding (README)` --references--> `src/etl_pipeline.py (task etl, spark-submit)`  [EXTRACTED]
  JOURNAL.md → CLAUDE.md
- `Livrable académique issue template` --references--> `hive-server service`  [INFERRED]
  .github/ISSUE_TEMPLATE/academic-deliverable.yml → compose.yaml
- `task jupyter` --references--> `jupyter service`  [INFERRED]
  Taskfile.yml → compose.yaml
- `Pull request template` --references--> `gitleaks hook`  [INFERRED]
  .github/PULL_REQUEST_TEMPLATE.md → .pre-commit-config.yaml
- `Architecture du projet (README)` --references--> `Chaîne Big Data CSV → HDFS → Spark → Hive → Jupyter`  [INFERRED]
  README.md → CLAUDE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **HDFS + Hive Docker stack** — compose_namenode, compose_datanode, compose_hive_metastore_postgresql, compose_hive_metastore, compose_hive_server, compose_jupyter [EXTRACTED 1.00]
- **Pre-commit quality gate** — pre_commit_config_ruff_hook, pre_commit_config_yamllint_hook, pre_commit_config_sqlfluff_lint_hook, pre_commit_config_gitleaks_hook, pre_commit_config_conventional_pre_commit_hook [EXTRACTED 1.00]
- **Artefacts couverts par la Definition of Done** — claude_definition_of_done, status_maintenance_rule, claude_latex_report_structure, journal_rapport_rattrapage [INFERRED 0.85]
- **Flux du pipeline ETL Spark (schema → cleaning → tables → hive_io)** — claude_etl_pipeline, claude_etl_schema_py, claude_etl_cleaning_py, claude_etl_tables_py, claude_etl_hive_io_py [INFERRED 0.85]
- **Doctrine de reproductibilité par épinglage (images, versions, dépendances)** — claude_pinned_images, claude_texlive_historic_image, security_pinned_dependencies, claude_hadoop_2_7_4_ports, claude_test_env_versions [INFERRED 0.85]
- **Taskfile command entry points** — taskfile_up, taskfile_ingest, taskfile_etl, taskfile_test, taskfile_report [INFERRED 0.85]

## Communities (51 total, 29 thin omitted)

### Community 0 - "internal task log"
Cohesion: 0.10
Nodes (26): bigdata bridge network, datanode service, hive-metastore service, hive-metastore-postgresql service, hive-server service, jupyter service, namenode service, datanode dev port override (+18 more)

### Community 1 - "pyspark_sql"
Cohesion: 0.13
Nodes (15): _hive_columns_ddl(), DataFrame, SparkSession, Écrit `df` en Parquet sur HDFS puis (re)crée la table Hive externe…, write_processed_table(), get_spark(), SparkSession, pyspark_sql (+7 more)

### Community 2 - "src/etl_pipeline.py (task etl, spark-submit)"
Cohesion: 0.16
Nodes (19): Chaîne Big Data CSV → HDFS → Spark → Hive → Jupyter, 120 doublons dans processed.competences (9548 → 9428), split(required_skills,'|') + explode(), Table competences, src/etl/cleaning.py (dédoublonnage + filtre salaire), src/etl/hive_io.py (Parquet HDFS + DDL externe), src/etl_pipeline.py (task etl, spark-submit), src/etl/schema.py (StructType RAW) (+11 more)

### Community 3 - "Images Docker pinnées (jamais :latest)"
Cohesion: 0.14
Nodes (15): colima sur Apple Silicon, Docker Compose modulaire (compose.yaml + override), Configuration .env / .env.example / env/hadoop-hive.env, Ports web Hadoop 2.7.4 : 50070/50075, postgres:13.18 backend metastore, JAVA_TOOL_OPTIONS=-Xint sur services JVM, Jupyter/PySpark remplace Zeppelin, Images Docker pinnées (jamais :latest) (+7 more)

### Community 4 - "État actuel — ce qui est FAIT et vérifié"
Cohesion: 0.15
Nodes (14): 6 services Compose + réseau bigdata, Minimum 6 visualisations dashboard, Barème /20 du sujet, Limites Hive 2.3.2 (pas de sous-requêtes scalaires ni CROSS JOIN), jupyter/pyspark-notebook:spark-3.5.0, Requêtes obligatoires Jour 1, Requêtes obligatoires Jour 2 (8), KPI obligatoires Jour 3 (10) (+6 more)

### Community 5 - "src/etl/tables.py"
Cohesion: 0.38
Nodes (6): build_competences(), build_metiers(), build_offres(), DataFrame, Une ligne par couple (job_id, compétence). dropDuplicates() : `required_skills`…, Référentiel des métiers distincts. metier_id est un hash déterministe…

### Community 6 - "screenshots_web.py"
Cohesion: 0.18
Nodes (10): fixture, os, playwright_sync_api, pytest, capture(), main(), Captures des interfaces web (HDFS NameNode, Jupyter) pour report/figures/.…, sys (+2 more)

### Community 7 - "Rapport LaTeX modulaire (main.tex + preamble/ + chapters/)"
Cohesion: 0.18
Nodes (12): Definition of Done (5 conditions), Rapport LaTeX modulaire (main.tex + preamble/ + chapters/), Nettoyage des issues GitHub (87 supprimées, #94-#104 recréées), Rattrapage rapport (Definition of Done, Étapes 1-2), Rapport chapitres 01/02 et 11-13 (issues #110, #111, #99), Corrections STATUS.md + recréation des issues GitHub, Structure du dépôt (README), Licence Apache 2.0 des polices (+4 more)

### Community 8 - "./run wrapper go-task containerisé"
Cohesion: 0.33
Nodes (9): Montage au chemin absolu hôte (sibling containers), Montage du socket Docker dans ./run, Dockerfile.runner (alpine + go-task + docker-cli), ./run wrapper go-task containerisé, Java 17-21 max + Python 3.12 pour pyspark==3.5.0, Test à blanc de l'onboarding (README), Wrapper ./run (go-task containerisé), Le wrapper ./run (README) (+1 more)

### Community 9 - "task screenshots-cli (freeze)"
Cohesion: 0.53
Nodes (6): Piège freeze -x timeout court (~2-3s), task screenshots-cli (freeze), task screenshots-web (Playwright), Taskfile.yml point d'entrée unique (go-task), Captures d'écran automatisées (issue #101), Référence complète des commandes Taskfile

### Community 10 - "gitleaks hook"
Cohesion: 0.47
Nodes (6): Pull request template, CI lint job, detect-private-key hook, gitleaks hook, task lint, task setup

### Community 11 - "pre-commit run --all-files obligatoire avant push"
Cohesion: 0.50
Nodes (5): pre-commit run --all-files obligatoire avant push, ruff + sqlfluff (Hive) + gitleaks, Audit de cohérence complet 16/09 + Project + issues rétroactives, Correction CI cassée après le push #95 (commit 2170739), Politique secrets / .env / gitleaks

### Community 12 - "Règles d'usage graphify (AGENTS.md)"
Cohesion: 0.50
Nodes (4): graphify-out/graph.json, graphify-out/GRAPH_REPORT.md, Règles d'usage graphify (AGENTS.md), graphify-out/wiki/index.md

### Community 13 - "screenshots_cli.sh"
Cohesion: 0.83
Nodes (3): capture(), render(), screenshots_cli.sh script

### Community 14 - "Tâche infra issue template"
Cohesion: 0.67
Nodes (3): Bug issue template, Tâche infra issue template, sync-status job

### Community 15 - "Périmètre de sécurité du projet"
Cohesion: 0.67
Nodes (3): Dataset Kaggle AI Jobs Market 2025-2026 | Salaries, Hors périmètre : durcissement production, auth multi-utilisateurs, chiffrement, Périmètre de sécurité du projet

### Community 36 - "scripts/etl_pipeline.py"
Cohesion: 0.25
Nodes (6): ambiguous_python_import_06e0261f223c, ambiguous_python_import_29f3e02a2e5a, ambiguous_python_import_b58c59440434, ambiguous_python_import_f6681c61a420, ambiguous_python_import_fe6f2a450636, Pipeline ETL RAW -> processed (offres, metiers, competences). Lit le CSV RAW…

### Community 37 - "src/etl_pipeline.py"
Cohesion: 0.25
Nodes (6): ambiguous_python_import_204c15ceae1b, ambiguous_python_import_261db20eff55, ambiguous_python_import_28b126591962, ambiguous_python_import_94f876289f70, ambiguous_python_import_b3f76cecd4eb, Pipeline ETL RAW -> processed (offres, metiers, competences). Lit le CSV RAW…

### Community 38 - "scripts/etl/tables.py"
Cohesion: 0.38
Nodes (6): build_competences(), build_metiers(), build_offres(), DataFrame, Une ligne par couple (job_id, compétence). dropDuplicates() : `required_skills`…, Référentiel des métiers distincts. metier_id est un hash déterministe…

### Community 40 - "scripts/etl/cleaning.py"
Cohesion: 0.47
Nodes (4): clean(), null_counts(), DataFrame, Nettoie le DataFrame RAW et retourne (df_cleaned, stats). stats contient les…

### Community 41 - "src/etl/cleaning.py"
Cohesion: 0.47
Nodes (4): clean(), null_counts(), DataFrame, Nettoie le DataFrame RAW et retourne (df_cleaned, stats). stats contient les…

### Community 42 - "Livrable final — Projet Big Data : Marché de l'emploi en IA 2025-2026"
Cohesion: 0.40
Nodes (4): Contenu du livrable, Livrable final — Projet Big Data : Marché de l'emploi en IA 2025-2026, Points de vigilance, Structure du livrable

## Knowledge Gaps
- **58 isolated node(s):** `projet_ia.ai_jobs_raw`, `bigdata-ai-jobs-market`, `01_ingest_hdfs.sh script`, `hive-metastore-entrypoint.sh script`, `projet_ia.ai_jobs_raw` (+53 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 128 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `État actuel — ce qui est FAIT et vérifié` connect `État actuel — ce qui est FAIT et vérifié` to `src/etl_pipeline.py (task etl, spark-submit)`, `Rapport LaTeX modulaire (main.tex + preamble/ + chapters/)`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `metier_id déterministe sha2(job_title,256)` connect `src/etl_pipeline.py (task etl, spark-submit)` to `État actuel — ce qui est FAIT et vérifié`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `Rapport LaTeX modulaire (main.tex + preamble/ + chapters/)` connect `Rapport LaTeX modulaire (main.tex + preamble/ + chapters/)` to `Images Docker pinnées (jamais :latest)`, `État actuel — ce qui est FAIT et vérifié`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `Rapport LaTeX modulaire (main.tex + preamble/ + chapters/)` (e.g. with `Polices Roboto et Poppins versionnées` and `Structure du dépôt (README)`) actually correct?**
  _`Rapport LaTeX modulaire (main.tex + preamble/ + chapters/)` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `projet_ia.ai_jobs_raw`, `bigdata-ai-jobs-market`, `01_ingest_hdfs.sh script` to the rest of the system?**
  _58 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `internal task log` be split into smaller, more focused modules?**
  _Cohesion score 0.09538461538461539 - nodes in this community are weakly interconnected._
- **Should `pyspark_sql` be split into smaller, more focused modules?**
  _Cohesion score 0.1286549707602339 - nodes in this community are weakly interconnected._