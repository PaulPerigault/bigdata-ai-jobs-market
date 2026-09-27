# Graph Report - bigdata-ai-jobs-market  (2026-09-27)

## Corpus Check
- Corpus is ~21,203 words - fits in a single context window. You may not need a graph.

## Summary
- 201 nodes · 242 edges · 36 communities (16 shown, 20 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 34 edges (avg confidence: 0.81)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Docker stack & Taskfile commands
- Spark ETL code & unit tests
- Data model & pipeline bugs
- Docker infra & image pinning
- Academic deliverables & KPIs
- Table builders & tests
- Web screenshot tooling
- Project process & LaTeX report
- ./run wrapper & task containerization
- CLI screenshots & Taskfile docs
- CI & pre-commit linting
- Commit quality policy
- Graphify tooling
- CLI screenshot script
- Issue templates & board sync
- Dataset & security scope
- YAML linting
- ./run script
- HDFS ingest script
- Hive RAW table DDL
- Conventional Commits
- Repository identity
- Large-file pre-commit hook
- Merge-conflict pre-commit hook
- check-yaml pre-commit hook
- end-of-file-fixer pre-commit hook
- mixed-line-ending pre-commit hook
- ruff-format pre-commit hook
- ruff pre-commit hook
- sqlfluff pre-commit hook
- trailing-whitespace pre-commit hook
- Loopback port binding

## God Nodes (most connected - your core abstractions)
1. `clean()` - 9 edges
2. `build_metiers()` - 8 edges
3. `build_competences()` - 8 edges
4. `main()` - 8 edges
5. `Rapport LaTeX modulaire (main.tex + preamble/ + chapters/)` - 8 edges
6. `internal task log` - 8 edges
7. `write_processed_table()` - 7 edges
8. `src/etl_pipeline.py (task etl, spark-submit)` - 7 edges
9. `Images Docker pinnées (jamais :latest)` - 7 edges
10. `namenode service` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Architecture du projet (README)` --references--> `Chaîne Big Data CSV → HDFS → Spark → Hive → Jupyter`  [INFERRED]
  README.md → CLAUDE.md
- `Test à blanc de l'onboarding (README)` --references--> `src/etl_pipeline.py (task etl, spark-submit)`  [EXTRACTED]
  JOURNAL.md → CLAUDE.md
- `Dépendances Python figées (pyproject.toml)` --references--> `Images Docker pinnées (jamais :latest)`  [INFERRED]
  SECURITY.md → CLAUDE.md
- `Rapport LaTeX modulaire (main.tex + preamble/ + chapters/)` --references--> `Polices Roboto et Poppins versionnées`  [INFERRED]
  CLAUDE.md → report/fonts/README.md
- `Structure du dépôt (README)` --references--> `Rapport LaTeX modulaire (main.tex + preamble/ + chapters/)`  [INFERRED]
  README.md → CLAUDE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Flux du pipeline ETL Spark (schema → cleaning → tables → hive_io)** — claude_etl_pipeline, claude_etl_schema_py, claude_etl_cleaning_py, claude_etl_tables_py, claude_etl_hive_io_py [INFERRED 0.85]
- **Artefacts couverts par la Definition of Done** — claude_definition_of_done, status_maintenance_rule, claude_latex_report_structure, journal_rapport_rattrapage [INFERRED 0.85]
- **Doctrine de reproductibilité par épinglage (images, versions, dépendances)** — claude_pinned_images, claude_texlive_historic_image, security_pinned_dependencies, claude_hadoop_2_7_4_ports, claude_test_env_versions [INFERRED 0.85]
- **HDFS + Hive Docker stack** — compose_namenode, compose_datanode, compose_hive_metastore_postgresql, compose_hive_metastore, compose_hive_server, compose_jupyter [EXTRACTED 1.00]
- **Pre-commit quality gate** — pre_commit_config_ruff_hook, pre_commit_config_yamllint_hook, pre_commit_config_sqlfluff_lint_hook, pre_commit_config_gitleaks_hook, pre_commit_config_conventional_pre_commit_hook [EXTRACTED 1.00]
- **Taskfile command entry points** — taskfile_up, taskfile_ingest, taskfile_etl, taskfile_test, taskfile_report [INFERRED 0.85]

## Communities (36 total, 20 thin omitted)

### Community 0 - "Docker stack & Taskfile commands"
Cohesion: 0.10
Nodes (26): bigdata bridge network, datanode service, hive-metastore service, hive-metastore-postgresql service, hive-server service, jupyter service, namenode service, datanode dev port override (+18 more)

### Community 1 - "Spark ETL code & unit tests"
Cohesion: 0.14
Nodes (17): pyspark_sql_types, clean(), null_counts(), print_stats(), DataFrame, Nettoie le DataFrame RAW et retourne (df_cleaned, stats). stats contient les…, _hive_columns_ddl(), DataFrame (+9 more)

### Community 2 - "Data model & pipeline bugs"
Cohesion: 0.16
Nodes (19): Chaîne Big Data CSV → HDFS → Spark → Hive → Jupyter, 120 doublons dans processed.competences (9548 → 9428), split(required_skills,'|') + explode(), Table competences, src/etl/cleaning.py (dédoublonnage + filtre salaire), src/etl/hive_io.py (Parquet HDFS + DDL externe), src/etl_pipeline.py (task etl, spark-submit), src/etl/schema.py (StructType RAW) (+11 more)

### Community 3 - "Docker infra & image pinning"
Cohesion: 0.14
Nodes (15): colima sur Apple Silicon, Docker Compose modulaire (compose.yaml + override), Configuration .env / .env.example / env/hadoop-hive.env, Ports web Hadoop 2.7.4 : 50070/50075, postgres:13.18 backend metastore, JAVA_TOOL_OPTIONS=-Xint sur services JVM, Jupyter/PySpark remplace Zeppelin, Images Docker pinnées (jamais :latest) (+7 more)

### Community 4 - "Academic deliverables & KPIs"
Cohesion: 0.15
Nodes (14): 6 services Compose + réseau bigdata, Minimum 6 visualisations dashboard, Barème /20 du sujet, Limites Hive 2.3.2 (pas de sous-requêtes scalaires ni CROSS JOIN), jupyter/pyspark-notebook:spark-3.5.0, Requêtes obligatoires Jour 1, Requêtes obligatoires Jour 2 (8), KPI obligatoires Jour 3 (10) (+6 more)

### Community 5 - "Table builders & tests"
Cohesion: 0.25
Nodes (11): build_competences(), build_metiers(), build_offres(), DataFrame, Une ligne par couple (job_id, compétence). dropDuplicates() : `required_skills`…, Référentiel des métiers distincts. metier_id est un hash déterministe…, test_row_counts_are_consistent_across_the_pipeline(), test_build_competences_deduplicates_repeated_skill_in_same_offer() (+3 more)

### Community 6 - "Web screenshot tooling"
Cohesion: 0.17
Nodes (11): fixture, os, playwright_sync_api, pyspark_sql, pytest, capture(), main(), Captures des interfaces web (HDFS NameNode, Jupyter) pour report/figures/.… (+3 more)

### Community 7 - "Project process & LaTeX report"
Cohesion: 0.18
Nodes (12): Definition of Done (5 conditions), Rapport LaTeX modulaire (main.tex + preamble/ + chapters/), Nettoyage des issues GitHub (87 supprimées, #94-#104 recréées), Rattrapage rapport (Definition of Done, Étapes 1-2), Rapport chapitres 01/02 et 11-13 (issues #110, #111, #99), Corrections STATUS.md + recréation des issues GitHub, Structure du dépôt (README), Licence Apache 2.0 des polices (+4 more)

### Community 8 - "./run wrapper & task containerization"
Cohesion: 0.33
Nodes (9): Montage au chemin absolu hôte (sibling containers), Montage du socket Docker dans ./run, Dockerfile.runner (alpine + go-task + docker-cli), ./run wrapper go-task containerisé, Java 17-21 max + Python 3.12 pour pyspark==3.5.0, Test à blanc de l'onboarding (README), Wrapper ./run (go-task containerisé), Le wrapper ./run (README) (+1 more)

### Community 9 - "CLI screenshots & Taskfile docs"
Cohesion: 0.53
Nodes (6): Piège freeze -x timeout court (~2-3s), task screenshots-cli (freeze), task screenshots-web (Playwright), Taskfile.yml point d'entrée unique (go-task), Captures d'écran automatisées (issue #101), Référence complète des commandes Taskfile

### Community 10 - "CI & pre-commit linting"
Cohesion: 0.47
Nodes (6): Pull request template, CI lint job, detect-private-key hook, gitleaks hook, task lint, task setup

### Community 11 - "Commit quality policy"
Cohesion: 0.50
Nodes (5): pre-commit run --all-files obligatoire avant push, ruff + sqlfluff (Hive) + gitleaks, Audit de cohérence complet 16/09 + Project + issues rétroactives, Correction CI cassée après le push #95 (commit 2170739), Politique secrets / .env / gitleaks

### Community 12 - "Graphify tooling"
Cohesion: 0.50
Nodes (4): graphify-out/graph.json, graphify-out/GRAPH_REPORT.md, Règles d'usage graphify (AGENTS.md), graphify-out/wiki/index.md

### Community 13 - "CLI screenshot script"
Cohesion: 0.83
Nodes (3): capture(), render(), screenshots_cli.sh script

### Community 14 - "Issue templates & board sync"
Cohesion: 0.67
Nodes (3): Bug issue template, Tâche infra issue template, sync-status job

### Community 15 - "Dataset & security scope"
Cohesion: 0.67
Nodes (3): Dataset Kaggle AI Jobs Market 2025-2026 | Salaries, Hors périmètre : durcissement production, auth multi-utilisateurs, chiffrement, Périmètre de sécurité du projet

## Knowledge Gaps
- **54 isolated node(s):** `bigdata-ai-jobs-market`, `01_ingest_hdfs.sh script`, `hive-metastore-entrypoint.sh script`, `projet_ia.ai_jobs_raw`, `src/etl/schema.py (StructType RAW)` (+49 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 85 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `État actuel — ce qui est FAIT et vérifié` connect `Academic deliverables & KPIs` to `Data model & pipeline bugs`, `Project process & LaTeX report`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `metier_id déterministe sha2(job_title,256)` connect `Data model & pipeline bugs` to `Academic deliverables & KPIs`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `Rapport LaTeX modulaire (main.tex + preamble/ + chapters/)` connect `Project process & LaTeX report` to `Docker infra & image pinning`, `Academic deliverables & KPIs`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `Rapport LaTeX modulaire (main.tex + preamble/ + chapters/)` (e.g. with `Polices Roboto et Poppins versionnées` and `Structure du dépôt (README)`) actually correct?**
  _`Rapport LaTeX modulaire (main.tex + preamble/ + chapters/)` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `bigdata-ai-jobs-market`, `01_ingest_hdfs.sh script`, `hive-metastore-entrypoint.sh script` to the rest of the system?**
  _54 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Docker stack & Taskfile commands` be split into smaller, more focused modules?**
  _Cohesion score 0.09538461538461539 - nodes in this community are weakly interconnected._
- **Should `Spark ETL code & unit tests` be split into smaller, more focused modules?**
  _Cohesion score 0.1422924901185771 - nodes in this community are weakly interconnected._