# Journal d'exécution

Trace des recettes Taskfile exécutées sur ce projet. Ajout en fin de
fichier uniquement (append) — ne jamais réorganiser ou supprimer une
entrée passée (voir CLAUDE.md).

## 2026-09-16 15:07 — task up (validation réelle Étape 1)
Commande : docker compose up -d (via colima, cf. CLAUDE.md)
Résultat : 6/6 services healthy (namenode, datanode, hive-metastore-postgresql,
hive-metastore, hive-server, jupyter). Vérifié en vrai : hdfs dfs -ls/-mkdir,
beeline SHOW DATABASES, et un job PySpark depuis Jupyter écrivant une table
Hive sur HDFS puis la relisant (round-trip HDFS -> Hive -> Spark confirmé).
Corrections apportées en cours de route : ports web namenode/datanode
(50070/50075, pas 9870/9864 — Hadoop 2.7.4), SERVICE_PRECONDITION datanode
(namenode:8020), backend Postgres remplacé par postgres:13.18 officiel
(bde2020/hive-metastore-postgresql crashait sous émulation), script
scripts/hive-metastore-entrypoint.sh pour initialiser le schéma Hive,
JAVA_TOOL_OPTIONS=-Xint pour contourner un blocage JIT sous QEMU.
Auteur : task automation

## 2026-09-16 15:35 — task ingest + task etl (validation réelle Étape 2)
Commande : bash scripts/01_ingest_hdfs.sh && spark-submit src/etl_pipeline.py
Résultat : CSV déposé dans /projet_ia/raw (1500 lignes de données vérifiées
ls/du/wc -l). Table projet_ia.ai_jobs_raw (EXTERNAL, TEXTFILE) créée et
interrogée via Beeline (COUNT=1500, AVG salaire=194892$). Pipeline ETL
exécuté pour de vrai : 0 doublon job_id, 0 salaire <=0 sur ce run, 25
métiers (processed.metiers), 1500 offres (processed.offres), 9548 liaisons
job_id<->compétence (processed.competences), toutes écrites en Parquet sur
HDFS /projet_ia/processed/ et exposées comme tables Hive externes.
Jointure offres<->metiers vérifiée via Beeline (top métier par volume :
LLM Engineer, 75 offres, salaire moyen 240960$).
Bug corrigé en cours de route : spark.sql lisant une table Hive TEXTFILE
n'honore pas skip.header.line.count (ligne d'en-tête comptée comme donnée,
1501 au lieu de 1500) -> etl_pipeline.py lit désormais le CSV RAW
directement depuis HDFS via spark.read.csv(header=True), cf. CLAUDE.md.
Auteur : task automation

## 2026-09-16 16:00 — rattrapage rapport (Definition of Done, Étapes 1-2)
Commande : xelatex -interaction=nonstopmode -halt-on-error main.tex (x2, depuis report/)
Résultat : ajout d'une section "Definition of Done" dans CLAUDE.md (s'applique
à toutes les étapes suivantes). Éclatement de rapport/rapport_esiea.tex
(monolithique, placeholders) en report/main.tex + report/preamble/*.tex +
report/chapters/*.tex, avec rédaction réelle des chapitres concernés par les
Étapes 1-2 : 03_architecture (stack réelle + 3 corrections de sécurité issues
du scan automatique), 04_ingestion_hdfs (arborescence + 1501 lignes vérifiées),
05_hive_raw (DDL + bug skip.header.line.count ignoré par spark.sql, 1501 vs
1500), 06_spark_quality (comptages NULL/doublons chiffrés), 07_construction_
tables (fix metier_id + 1500 offres/25 metiers/9548 competences),
08_analyses (jointure offres<->metiers, LLM Engineer commenté). Compilation
vérifiée réellement (2 passes xelatex, 0 erreur, PDF 22 pages, polices Roboto/
Poppins versionnées dans report/fonts/ pour ne pas dépendre de l'install
système). Chapitres non encore concernés (01,02,09-15) laissés en placeholder,
normal tant que leur étape n'est pas atteinte.
Auteur : task automation

## 2026-09-16 16:15 — STATUS.md corrigé + issues GitHub recréées
Commande : gh issue delete/create/edit (voir historique de la session)
Résultat : corrections d'exactitude dans STATUS.md (pre-commit = ruff
seul, pas black ; GRANT_SUDO retiré du conteneur jupyter uniquement,
pas "conteneurs Hadoop" ; 9548 competences = chiffre exact, pas une
approximation ; label "sql" retiré du ticket 1, hors liste des 7 labels
approuvés). Ajout d'une 5e condition à la Definition of Done (CLAUDE.md)
: STATUS.md doit être mis à jour à chaque étape. Note ajoutée au ticket
"Captures d'écran" listant précisément les 4 captures manquantes
(report/figures/ vide, confirmé). 87 issues GitHub préexistantes
(CLOSED, ancienne architecture k3d/Zeppelin) supprimées après
confirmation utilisateur, labels pipeline/analytics/dashboard/rapport/
figures/qualité/livraison créés, 11 tickets de STATUS.md recréés en
issues #94-#104 (une erreur d'indexation de tableau bash a d'abord
décalé titres/labels vs corps de plusieurs issues — détectée et
corrigée avant validation finale). STATUS.md mis à jour avec les liens
vers chaque issue.
Auteur : task automation

## 2026-09-16 16:20 — Requêtes Hive SQL/Spark SQL manquantes (issue #103)
Commande : beeline -f sql/hive/01_analyses.sql ; spark-submit (comparaison)
Résultat : jointure offres<->competences dédiée exécutée pour de vrai
(top compétence Python, 942/1500 offres soit 63%). Requête GROUP BY +
HAVING exécutée (12 pays avec >50 offres et salaire moyen >150000$, USA
en tête à 226190$). Comparaison Hive SQL vs Spark SQL sur la même
requête (salaire moyen par expérience) : résultats identiques sur les 2
moteurs, Hive-on-MR 33.0s vs Spark SQL 8.8s (SparkSession chaude
comprise) - chiffré et documenté au chapitre 08. Rapport recompilé (2
passes xelatex, 0 erreur, 22 -> 24 pages). Issue #103 fermée, ticket
correspondant dans STATUS.md déplacé vers "fait".
Auteur : task automation
