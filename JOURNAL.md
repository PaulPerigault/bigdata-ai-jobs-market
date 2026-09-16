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
