# CLAUDE.md

Ce fichier cadre toute intervention de Claude Code sur ce dépôt. Le lire
intégralement avant toute action, et le respecter même si une demande
ponctuelle semble aller plus vite en le contournant.

## Contexte du projet

Projet pédagogique ESIEA (module Fondamentaux du Big Data, sujet proposé
par M. Touati Zouhaier) : construire une chaîne Big Data complète pour
analyser le marché de l'emploi en IA 2025-2026 à partir du dataset
`ai_jobs_market_2025_2026.csv` (1500 lignes, 25 colonnes — vérifié sur
le fichier réel).

- Équipe de 5 personnes, travail en parallèle sur le même dépôt.
- Deadline : 21/09/2026.
- Rapport final en LaTeX aux couleurs ESIEA (`report/main.tex` + chapitres
  dans `report/chapters/`, voir section « Rapport LaTeX modulaire » plus
  bas), produit en parallèle du code — ne jamais le considérer comme
  secondaire. **Voir « Definition of Done » ci-dessous : un chapitre
  n'attend jamais la fin du projet pour être rédigé.**
- Un `JOURNAL.md` à la racine trace l'exécution (voir plus bas) : toute
  tâche significative doit y ajouter une entrée.

**Objectif de fond** : un projet qui a l'air et se comporte comme un
projet d'ingénieur (reproductible, versionné, testé), pas comme un TP
cliqué à la main. Mais rester proportionné à 5 jours et 5 personnes —
ne pas ajouter de complexité qui ne sert pas le rendu.

## Definition of Done (s'applique à chaque étape, à partir de maintenant)

Le rapport a pris du retard sur le code une première fois (Étapes 1 et
2 rattrapées après coup) — cette section existe pour que ça ne se
reproduise pas. Elle s'applique à **chaque** étape du plan (Étape 2, 3,
4, 5...), sans qu'il soit besoin de le redemander à chaque fois : c'est
la norme du projet. Une étape n'est considérée terminée que si les 5
conditions suivantes sont remplies :

1. **Le code/l'infra correspondant fonctionne et est testé
   réellement** — pas seulement « ça devrait marcher » : commande
   exécutée pour de vrai, sortie vérifiée (cf. les validations réelles
   des Étapes 1 et 2 comme référence de rigueur attendue).
2. **Le(s) chapitre(s) du rapport concernés
   (`report/chapters/*.tex`) sont rédigés avec les résultats réels
   obtenus à cette étape** — chiffres réels, requêtes réelles,
   captures/sorties réelles. Jamais de placeholder ni de
   « à compléter plus tard » sur un chapitre couvert par une étape
   terminée.
3. **Toute décision technique qui s'écarte du plan initial** (bug
   corrigé, config changée, choix différent de ce qui était prévu) est
   documentée **à la fois** dans `CLAUDE.md` (déjà la norme) **et**
   dans le chapitre du rapport pertinent, avec la justification — le
   rapport doit pouvoir raconter la même histoire que `CLAUDE.md`, pas
   une version idéalisée qui passe sous silence les détours réels.
4. **`JOURNAL.md` a une entrée pour l'étape** (append-only, comme déjà
   spécifié plus bas).
5. **`STATUS.md` est mis à jour** : la section « État actuel » reflète
   le nouvel état réel (fichiers présents, chapitres réellement
   rédigés vs placeholder, requêtes réellement exécutées), et le ou les
   tickets correspondants sont déplacés de « Ce qu'il reste à faire »
   vers « fait » (coché `[x]`). `STATUS.md` doit rester aussi fiable
   que `CLAUDE.md` — jamais laissé dériver de l'état réel du repo.

Si une étape touche plusieurs chapitres, **tous** doivent être à jour
avant de passer à l'étape suivante — ne pas en oublier un parce qu'il
semblait secondaire.

## Architecture retenue (ne pas dévier sans validation)

```
CSV (data/raw/) → HDFS /projet_ia/raw
                 → Spark : contrôle, nettoyage, transformation
                 → HDFS /projet_ia/processed/{offres,metiers,competences}
                 → Hive (tables externes RAW + processed)
                 → Jupyter/PySpark (exploration, requêtes Hive SQL/Spark SQL, dashboard)
```

- **Jupyter/PySpark remplace Zeppelin** — choix validé avec le professeur.
  Ne jamais réintroduire Zeppelin/DAS dans la stack.
- **HDFS et Hive restent obligatoires**, même si l'analyse finale se fait
  dans Jupyter. Ne jamais lire le CSV directement depuis le système de
  fichiers local dans le notebook final : toujours passer par HDFS → Hive
  (ou Spark lisant HDFS), sinon les points HDFS/Hive du barème sont perdus.
- Stack orchestrée via **Docker Compose modulaire** :
  `compose.yaml` (services de base) + `compose.override.yaml` (overrides
  dev local). Jamais un seul fichier monolithique.
- **Taskfile.yml** (go-task) est le seul point d'entrée documenté :
  `task up`, `task down`, `task ingest`, `task etl`, `task test`,
  `task hive-shell`, `task jupyter`. Ne pas demander aux membres de
  l'équipe de retenir des commandes `docker compose exec ...` à la main.

### Règles Docker Compose
- Images **toujours pinnées** par tag précis (jamais `:latest`).
- `healthcheck` sur chaque service ; les dépendances utilisent
  `depends_on: condition: service_healthy`, pas un simple `depends_on` nu.
- `deploy.resources.limits` raisonnables (l'équipe tourne sur des laptops,
  pas des serveurs).
- Secrets et config variables dans `.env` (gitignored) ; `.env.example`
  versionné avec des valeurs factices.

## Modèle de données cible

Table `offres` : une ligne par offre. Colonnes clés : `job_id`,
`metier_id` (FK), `experience_level`, `years_of_experience`,
`annual_salary_usd`, `salary_min_usd`, `salary_max_usd`, `city`,
`country`, `remote_work`, `company_size`, `industry`,
`ai_salary_premium_pct`, `demand_score`, `posting_year`, `posting_month`.

Table `metiers` : une ligne par `job_title` distinct.
**`metier_id` doit être stable et déterministe** — ne jamais utiliser
`monotonically_increasing_id()` (non stable entre exécutions/partitions).
Utiliser un hash déterministe, ex. `sha2(job_title, 256)` tronqué, ou un
`row_number()` sur un tri stable (`ORDER BY job_title`).

Table `competences` : `job_id` + une ligne par compétence, obtenue via
`split(required_skills, '\\|')` puis `explode()`.

Nettoyage à documenter et **chiffrer** (pas juste appliqué en silence) :
- Comptage des NULLs par colonne importante, avant/après nettoyage.
- Comptage des doublons sur `job_id` avant/après `dropDuplicates`.
- Toute règle de filtrage (ex. salaires ≤ 0) doit logger le nombre de
  lignes affectées.

## Livrables obligatoires (à ne jamais oublier en cours de route)

Le barème est sur 20 points, réparti HDFS (2) / Hive RAW+processed (3) /
Spark nettoyage (4) / modèle 3 tables (3) / Hive SQL+Spark SQL (3) /
visualisations (3) / analyse et rapport (2). Concrètement :

- Requêtes obligatoires Jour 1 : nombre d'offres, métiers distincts, pays
  distincts, salaire moyen/min/max, répartition par expérience.
- Requêtes obligatoires Jour 2 (8) : top 10 métiers par offres, salaire
  moyen par métier, top 10 compétences, salaire moyen par expérience,
  offres par pays/secteur, **jointure offres↔metiers** (requête dédiée,
  pas seulement utilisée en interne), **jointure offres↔competences**
  (idem), une requête GROUP BY + HAVING.
- KPI obligatoires Jour 3 (10) : total offres/métiers, salaire moyen ET
  médian (`percentile_approx`), top métiers les mieux rémunérés, top
  métiers les plus demandés, top compétences, salaire moyen par pays,
  salaire par expérience, répartition télétravail/présentiel
  (`remote_work`), analyse LLM/GenAI (`is_llm_role`), évolution
  2025-2026 par période (`posting_year`/`posting_month`).
- **Au moins 4 analyses au choix** en plus des KPI obligatoires.
- **Au moins 6 visualisations** dans le dashboard, chacune avec titre,
  requête source identifiable, interprétation chiffrée affichée.
- Comparer, quand pertinent, une requête Hive SQL et son équivalent
  Spark SQL (section 8 du rapport).
- Rapport final : 6-10 constats, 3 recommandations argumentées, une
  section limites de l'étude distincte de la synthèse.

## Conventions de dépôt

- Commits **Conventional Commits** (`feat:`, `fix:`, `chore:`, `docs:`,
  `test:`). Historique lisible = preuve de démarche pour le rapport.
- `pre-commit` obligatoire avant push : `ruff` (lint + format, pas de
  black), `sqlfluff` (SQL), `gitleaks` (scan de secrets). **Toujours
  lancer `pre-commit run --all-files` avant de commit/push, pas
  seulement sur les fichiers touchés** — un run scopé a laissé la CI
  cassée sur `src/*.ipynb` pendant plusieurs commits sans que personne
  ne le remarque (voir audit du 16/09/2026, `JOURNAL.md`). Ne jamais
  committer avec `--no-verify` sauf urgence explicitement assumée par
  l'auteur.
- Transformations Spark versionnées en **scripts `.py` dans `src/`**, pas
  seulement écrites à la volée dans le notebook. Le notebook final
  importe/appelle ces scripts ou reproduit leurs étapes de façon
  traçable — il ne doit pas être le seul endroit où vit la logique.
- Tests dans `tests/` (pytest) : au minimum des sanity checks de comptage
  de lignes après chaque étape ETL (`test_row_counts.py`), et une
  validation de schéma sur les 3 tables cibles.
- `data/raw/` et `.env` dans `.gitignore` dès le premier commit — ne
  jamais committer le CSV brut ni des secrets.

## JOURNAL.md

Chaque recette Taskfile qui exécute une étape significative
(ingestion, ETL, création de tables Hive, run de tests) doit ajouter une
entrée à `JOURNAL.md` à la racine, au format :

```
## AAAA-MM-JJ HH:MM — task <nom>
Commande : <commande exécutée>
Résultat : <ce qui a été vérifié, ex. nombre de lignes>
Auteur : <nom ou "task automation">
```

Ne pas réécrire l'historique de ce fichier ; toujours ajouter en fin de
fichier (append), jamais réorganiser ou supprimer des entrées passées.

## Pipeline ETL (Étape 2) — validé réellement (`task ingest` + `task etl`)

- `scripts/01_ingest_hdfs.sh` dépose `data/raw/ai_jobs_market_2025_2026.csv`
  dans `/projet_ia/raw` (HDFS) et vérifie ls/du/wc -l (1500 lignes de
  données + 1 en-tête).
- `sql/hive/00_create_raw_table.sql` crée `projet_ia.ai_jobs_raw`
  (EXTERNAL, TEXTFILE, colonnes typées — le CSV n'a aucune virgule/quote
  interne, un SerDe délimité simple suffit).
- **`skip.header.line.count` n'est PAS honoré quand Spark lit une table
  Hive TEXTFILE via `spark.sql("SELECT * FROM ...")`** (vérifié : la
  ligne d'en-tête remonte comme une ligne de données, 1501 au lieu de
  1500). `src/etl_pipeline.py` lit donc le CSV RAW directement depuis
  HDFS via `spark.read.csv(header=True, schema=...)` — toujours conforme
  à la règle « jamais lire le CSV en local, toujours HDFS → Hive *ou*
  Spark lisant HDFS » (la parenthèse autorise explicitement ce chemin).
  La table Hive RAW reste le point d'entrée pour les requêtes Hive SQL
  (barème), pas pour ce script de transformation.
- `src/etl/` : `schema.py` (StructType RAW), `cleaning.py` (dédoublonnage
  + filtre salaire + comptages NULL avant/après, chiffrés), `tables.py`
  (construction `offres`/`metiers`/`competences` — **`metier_id` en
  `sha2(job_title, 256)` tronqué à 16 caractères**, jamais
  `monotonically_increasing_id()`), `hive_io.py` (écrit le Parquet sur
  HDFS puis dérive le DDL `CREATE EXTERNAL TABLE` depuis le schéma Spark).
- `src/etl_pipeline.py` (point d'entrée de `task etl`, exécuté via
  `spark-submit` dans le conteneur `jupyter`) écrit
  `/projet_ia/processed/{offres,metiers,competences}` et crée les 3
  tables Hive externes correspondantes dans la base `processed`.
- Chiffres de référence sur le dataset réel : 1500 lignes RAW, 0 doublon
  `job_id`, 0 ligne avec salaire ≤ 0 (le dataset est propre sur ce
  critère — le filtre reste actif et testé sur données synthétiques,
  voir `tests/unit/test_cleaning.py`), 25 métiers distincts, 1500
  offres, 9548 liaisons job_id↔compétence (chiffre exact). Jointure
  `processed.offres` ↔ `processed.metiers` vérifiée via Beeline (ex.
  LLM Engineer : 75 offres, salaire moyen 240 960 $).
- Tests dans `tests/unit/` (`test_cleaning.py`, `test_tables.py`,
  `test_row_counts.py`) : Spark local (`local[2]`, pas de Hive), aucune
  dépendance à la stack Compose — c'est ce que `task test` et le job CI
  `test` exécutent.

## Rapport LaTeX modulaire — structure réelle

Le rapport vivait initialement dans un unique fichier
`rapport/rapport_esiea.tex` (squelette 16 chapitres, tous en
placeholder). Éclaté en amont de l'Étape 5 (nécessaire pour appliquer
la Definition of Done dès l'Étape 2) :

- `report/main.tex` : `\documentclass` + `\input` des 3 fichiers de
  préambule puis des 15 chapitres, dans l'ordre.
- `report/preamble/{colors,fonts,style}.tex` : couleurs charte ESIEA,
  polices, mise en page/titleformat/tcolorbox — **ne pas modifier le
  fond (couleurs/polices) sans validation**, voir plus haut.
- `report/fonts/{Roboto,Poppins}-*.ttf` : polices versionnées (licence
  Apache, Google Fonts) et chargées via `Path=fonts/` dans
  `preamble/fonts.tex` — la compilation ne doit **pas** dépendre de
  polices installées système sur la machine de chaque membre.
- `report/chapters/NN_slug.tex` (`01_introduction.tex` …
  `15_annexes.tex`) : un chapitre = un fichier, numérotation qui
  correspond à l'ordre `\input` dans `main.tex`. Chapitres avec contenu
  réel à ce jour : `03_architecture`, `04_ingestion_hdfs`,
  `05_hive_raw`, `06_spark_quality`, `07_construction_tables`,
  `08_analyses`, `09_metiers_salaires` (Étapes 1-3, KPI Jour 3 inclus).
  Les autres restent en placeholder jusqu'à l'étape qui les concerne
  — normal, pas un oubli.
- Compilation vérifiée avec `xelatex -interaction=nonstopmode
  -halt-on-error main.tex` (2 passes, depuis `report/`) — via
  `mactex-no-gui` en local pour l'instant. Le conteneur `task report`
  documenté dans l'Étape 5 du plan initial (image texlive pinnée) reste
  à faire ; ne pas le considérer comme déjà en place.

## Ce que Claude Code ne doit PAS faire

- Ne pas réintroduire Zeppelin/DAS.
- Ne pas lire le CSV directement en local dans le pipeline final (HDFS
  obligatoire).
- Ne pas utiliser `:latest` sur une image Docker.
- Ne pas committer `data/raw/*.csv`, `.env`, ou tout fichier listé dans
  `.gitignore`.
- Ne pas fusionner/simplifier `compose.yaml` en un seul fichier monolithique.
- Ne pas modifier la structure du préambule du rapport
  (`report/preamble/{colors,fonts,style}.tex`) en dehors de son contenu
  (couleurs/polices de la charte ESIEA à respecter).
- Ne pas supprimer d'entrées existantes dans `JOURNAL.md`.
- Ne pas avancer à l'étape suivante du plan sans avoir satisfait la
  Definition of Done ci-dessous pour l'étape en cours.

## Stack technique de référence

Docker Compose (HDFS namenode/datanode, Hive metastore + server, Spark,
Jupyter/PySpark) · Taskfile (go-task) · Python (PySpark, pytest, ruff) ·
Hive SQL / Spark SQL · LaTeX (XeLaTeX, rapport aux couleurs ESIEA) ·
pre-commit + gitleaks.

### Images pinnées (socle infra, Étape 1) — validé réellement avec `task up`

Combo `bde2020` volontairement figé sur Hadoop 2.7.4 (pas 3.2.1) car
c'est la version pour laquelle l'image `bde2020/hive:2.3.2-postgresql-metastore`
est construite et testée — mélanger avec un namenode/datanode 3.2.1
aurait cassé la compatibilité RPC HDFS côté Hive sans bénéfice.

- `bde2020/hadoop-namenode:2.0.0-hadoop2.7.4-java8`,
  `bde2020/hadoop-datanode:2.0.0-hadoop2.7.4-java8`. **Ports web réels en
  Hadoop 2.7.4 : 50070 (namenode) et 50075 (datanode), pas 9870/9864**
  (défauts Hadoop 3.x) — healthchecks et `compose.override.yaml` alignés
  sur 50070/50075. `SERVICE_PRECONDITION` du datanode pointe sur
  `namenode:8020` (RPC), le port 9870 n'existe pas sur cette image.
- `bde2020/hive:2.3.2-postgresql-metastore` pour `hive-metastore`
  (service metastore Thrift, port 9083) **et** `hive-server`
  (HiveServer2, ports 10000 JDBC / 10002 web), même image, commande
  différente.
- **Backend Postgres du metastore : `postgres:13.18` (officiel), pas
  `bde2020/hive-metastore-postgresql:2.3.0`** — ce dernier embarque un
  entrypoint Go ancien qui crashe (`fatal error: newosproc`) sous
  émulation amd64→arm64 (Apple Silicon via colima/QEMU). Contrepartie :
  l'image officielle part d'une base `metastore` vide (pas de schéma
  Hive pré-chargé) — `hive-metastore` monte
  `scripts/hive-metastore-entrypoint.sh` et l'utilise comme `command`
  pour lancer `schematool -dbType postgres -initSchema` puis
  `hive --service metastore`. Ce script doit rester un **seul token**
  dans `command:` : l'`entrypoint.sh` de l'image `bde2020/hive` fait un
  `exec $@` non quoté qui découpe (et casse) toute commande contenant
  des espaces — ne jamais remettre un `sh -c "... ; ..."` inline ici.
  Identifiants Postgres attendus : `hive`/`hive`/`metastore`
  (voir `.env.example`), cohérents avec les
  `HIVE_SITE_CONF_javax_jdo_option_*` répétés dans l'`environment:` de
  `hive-metastore` **et** `hive-server` (ces deux services définissent
  aussi `SERVICE_PRECONDITION` dans leur propre `environment:`, ce qui
  écrase entièrement celui d'un anchor YAML fusionné via `<<:` — pas de
  deep merge en YAML — d'où la duplication au lieu d'un anchor commun).
- `JAVA_TOOL_OPTIONS=-Xint` sur tous les services JVM (namenode,
  datanode, hive-metastore, hive-server) — sous émulation QEMU
  (amd64 sur Apple Silicon), le JIT HotSpot provoque des blocages
  CPU-pinné de plusieurs minutes au premier lancement (`hdfs namenode
  -format`, `schematool`). Le mode interprété évite le bug, démarrage
  plus lent mais fiable. À retirer seulement si toute l'équipe tourne
  sur du x86_64 natif.
- `jupyter/pyspark-notebook:spark-3.5.0` pour le service `jupyter`
  (PySpark local, connecté à HDFS via `fs.defaultFS=hdfs://namenode:8020`
  et à Hive via `thrift://hive-metastore:9083`) — multi-arch, tourne
  nativement sur Apple Silicon, aucun souci d'émulation constaté.
- Config Hadoop/Hive non secrète versionnée dans `env/hadoop-hive.env`
  (traduite en XML par les entrypoints bde2020) ; identifiants Postgres
  et token Jupyter dans `.env` (voir `.env.example`).
- Réseau Compose unique : `bigdata`. Volumes nommés :
  `hadoop_namenode`, `hadoop_datanode`, `hive_metastore_postgresql`.
- `compose.override.yaml` ne porte que du confort de dev (ports web
  HDFS exposés sur 50070/50075, montage `./src` dans le conteneur
  Jupyter) — jamais requis pour que la stack tourne.
- Tags `.pre-commit-config.yaml` : `gitleaks` remplace `detect-secrets`
  (plus de `.secrets.baseline` à maintenir) ; `sqlfluff` ajouté avec
  dialecte `hive` (`.sqlfluff` à la racine), utilisé depuis l'Étape 3 par
  `sql/hive/01_analyses.sql` et `02_kpis.sql`.

### Tests locaux (`task test` / CI) — Java et Python requis

`pyspark==3.5.0` (voir `pyproject.toml`, extra `test`) ne démarre pas sous
un JDK ≥ 21 en local (`UnsupportedOperationException: getSubject is not
supported`, API retirée) ni sous Python ≥ 3.13 (crash du sérialiseur
cloudpickle) — utiliser **Java 17 ou 21 max** (`brew install
openjdk@21`, `export JAVA_HOME=/opt/homebrew/opt/openjdk@21`) et
**Python 3.12** pour l'environnement virtuel local. Le CI GitHub Actions
utilise déjà `actions/setup-java` (Java 17) et `actions/setup-python`
(3.12) — aucun changement nécessaire côté workflow, seulement côté poste
de dev local si `java -version` par défaut est plus récent.

### Docker sur Mac Apple Silicon (M-series) — colima, pas forcément Docker Desktop

Les images `bde2020/*` sont **amd64 uniquement** (pas d'image arm64) :
sur Apple Silicon elles tournent sous émulation QEMU, plus lentes qu'en
natif mais fonctionnelles une fois `JAVA_TOOL_OPTIONS=-Xint` en place
(voir ci-dessus). `docker compose up` a été validé pour de vrai sur ce
poste via **colima** (`brew install colima docker-compose`, puis
`colima start --cpu 4 --memory 8 --disk 60`) plutôt que Docker Desktop
(cask présent mais cassé sur cette machine — `Docker.app` absent malgré
l'installation Homebrew). Si `docker compose` n'est pas reconnu après
installation de `docker-compose` en formule brew, ajouter
`"cliPluginsExtraDirs": ["/opt/homebrew/lib/docker/cli-plugins"]` à
`~/.docker/config.json`. Chaque membre de l'équipe doit disposer d'un
runtime Docker fonctionnel (Docker Desktop **ou** colima) — peu importe
lequel, seul `docker compose` doit répondre.
