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

## Prérequis (versions vérifiées, pas génériques)

- **Docker + Docker Compose v2** (le plugin intégré `docker compose`,
  pas l'outil autonome `docker-compose` v1) — vérifié avec Docker
  Engine 29.8.1 / Compose plugin v5.5.1. Sur Apple Silicon, la stack a
  été validée via [colima](https://github.com/abiosoft/colima)
  (`brew install colima docker-compose`) plutôt que Docker Desktop —
  voir `CLAUDE.md` pour le détail (Docker Desktop peut fonctionner
  aussi, non testé spécifiquement sur ce projet).
- **RAM allouée au moteur Docker : 8 Go minimum**, validée réellement
  via `colima start --cpu 4 --memory 8 --disk 60`. À titre indicatif,
  la somme des `deploy.resources.limits.memory` des 6 services
  (`compose.yaml`) représente **~10,6 Go** (namenode 1,5 + datanode 1,5
  + hive-metastore-postgresql 0,5 + hive-metastore 1,5 + hive-server
  1,5 + jupyter 4) : ce sont des plafonds par conteneur, pas la RAM
  réellement consommée en simultané (d'où le fait que 8 Go suffisent en
  pratique), mais ne descendez pas en dessous sans marge si votre
  machine tourne d'autres services lourds en parallèle.
- [`go-task`](https://taskfile.dev/) (`brew install go-task`).
- **Python 3.12 exact** pour les tests locaux (`pyspark==3.5.0` ne
  démarre pas sous Python ≥ 3.13) **et Java 17 ou 21 exact** (pas plus
  récent — `pyspark==3.5.0` échoue sous un JDK ≥ 22 avec
  `UnsupportedOperationException: getSubject is not supported`). Si
  votre `python3`/`java` par défaut sont plus récents (fréquent avec
  Homebrew qui pointe vers la dernière version), installez les bonnes
  versions en parallèle sans les remplacer :

  ```bash
  brew install python@3.12 openjdk@21
  ```

  Voir l'étape 7 ci-dessous pour les utiliser explicitement sans
  changer votre `python3`/`java` global.

## Démarrage — de zéro à ça marche

Parcours testé dans cet ordre exact. Ne sautez pas d'étape : chacune
dépend de la précédente.

**1. Cloner le dépôt**

```bash
git clone https://github.com/PaulPerigault/bigdata-ai-jobs-market.git
cd bigdata-ai-jobs-market
```

**2. Récupérer le dataset (non fourni dans le dépôt)**

Le CSV `ai_jobs_market_2025_2026.csv` est **volontairement absent du
dépôt** (`data/raw/` est gitignored, voir `.gitignore` et
`SECURITY.md`). Sans cette étape, `task ingest` échouera avec un
fichier introuvable.

- Télécharger le dataset **AI Jobs Market 2025-2026 | Salaries** sur
  Kaggle : <https://www.kaggle.com/datasets/alitaqishah/ai-jobs-market-2025-2026-salaries>
  (compte Kaggle gratuit requis pour télécharger).
- Placer le fichier CSV extrait à l'emplacement exact attendu :

  ```bash
  mkdir -p data/raw
  mv ~/Downloads/ai_jobs_market_2025_2026.csv data/raw/ai_jobs_market_2025_2026.csv
  ```

  Le nom de fichier doit être exactement `ai_jobs_market_2025_2026.csv`
  (c'est le nom que `scripts/01_ingest_hdfs.sh` référence directement) —
  renommez-le si l'archive Kaggle le nomme différemment.

**3. Configurer l'environnement**

`task up` copie automatiquement `.env.example` vers `.env` s'il est
absent (voir la recette `up` dans `Taskfile.yml`) — vous n'êtes donc
**pas bloqué** si vous oubliez cette étape. Mais si vous voulez
personnaliser un identifiant avant le premier démarrage (rare, les
valeurs par défaut suffisent pour un usage local), faites-le vous-même
avant `task up` :

```bash
cp .env.example .env
```

**4. Démarrer la stack**

```bash
task up
```

Démarre HDFS (namenode/datanode), Hive (metastore + server, Postgres)
et Jupyter/PySpark via Docker Compose. Premier démarrage lent (images à
télécharger, plusieurs Go) ; les démarrages suivants sont rapides
(images/volumes déjà en cache). Vérifiez que les 6 services sont
`healthy` :

```bash
docker compose ps
```

Sous émulation (Apple Silicon via colima/QEMU), il arrive que
`datanode` crashe au tout premier démarrage (`exited (139)`,
segfault JVM pendant le JIT — voir `JAVA_TOOL_OPTIONS=-Xint` dans
`CLAUDE.md`) : relancez simplement `docker compose up -d`, ça repart
sans intervention. Si `task up` remonte une erreur de dépendance
(`dependency datanode failed to start`), c'est ce cas — un simple
`docker compose up -d` supplémentaire suffit.

**5. Ingérer le CSV dans HDFS**

```bash
task ingest
```

Dépose le CSV dans `/projet_ia/raw` sur HDFS et vérifie le dépôt
(`ls`/`du`/`wc -l`, 1500 lignes de données + 1 en-tête attendues).

**6. Lancer le pipeline ETL Spark**

```bash
task etl
```

Nettoie, transforme et écrit les tables `offres`/`metiers`/`competences`
sur HDFS (`/projet_ia/processed/`) puis les expose comme tables Hive
externes (base `processed`).

**7. Lancer les tests**

`task test` fait un simple `pip install -e ".[test]"` puis `pytest` —
il suppose que `pip`/`python`/`java` actifs dans votre shell pointent
déjà vers les bonnes versions (étape « Prérequis » ci-dessus). Si votre
`python3`/`java` par défaut sont plus récents, créez un environnement
virtuel dédié et activez-le **avant** de lancer `task test` (sinon vous
obtiendrez `ModuleNotFoundError`/`pip: command not found` ou un crash
PySpark selon la version active) :

```bash
python3.12 -m venv .venv
source .venv/bin/activate
export JAVA_HOME=/opt/homebrew/opt/openjdk@21
export PATH="$JAVA_HOME/bin:$PATH"
task test
```

Tests unitaires (`tests/unit/`, Spark local `local[2]`) — ne nécessitent
pas la stack Docker démarrée, peuvent être lancés indépendamment des
étapes 4-6.

**8. Compiler le rapport**

```bash
task report
```

Compile `report/main.tex` en PDF via un conteneur XeLaTeX pinné —
aucune installation LaTeX locale requise. Résultat dans
`report/main.pdf`.

## Utilisation — Taskfile (référence complète)

Toutes les commandes passent par `task`, seul point d'entrée documenté :

| Commande | Rôle |
|---|---|
| `task setup` | Installe les dépendances locales (pre-commit, venv de test). |
| `task up` | Démarre la stack Docker Compose (HDFS, Hive, Jupyter) — copie `.env.example` en `.env` si absent. |
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
